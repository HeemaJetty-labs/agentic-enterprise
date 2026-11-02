# Stage 1: Build Stage
FROM python:3.13-slim-bookworm AS builder
WORKDIR /app

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
build-essential \
&& rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Runtime Stage
FROM python:3.13-slim-bookworm AS runtime

# Create a non-root user for security
RUN groupadd -r agentuser && useradd -r -g agentuser agentuser

WORKDIR /app

# Copy only the installed packages from the builder
COPY --from=builder /install /usr/local
COPY . .

# Set ownership to the non-root user
RUN chown -R agentuser:agentuser /app
USER agentuser
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]