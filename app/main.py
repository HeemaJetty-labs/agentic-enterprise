from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1 import health
from fastapi import FastAPI, HTTPException
from schemas import AgentRequest, AgentResponse  # Import our new bouncers
import uuid
import logging

# Setup professional logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("enterprise_agent")


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Startup: This is where we will eventually initialize our LangGraph agents
    logger.info("Initializing Sovereign Agentic Core...")
    yield

# Shutdown: Clean up resources (DB connections, etc.)
logger.info("Shutting down Sovereign Agentic Core...")

# app = FastAPI(
#     title="Sovereign Enterprise Agent API",
#     version="0.1.0",
#     lifespan=lifespan
# )
app = FastAPI(title="Sovereign Agentic API",
              version="0.1.0", lifespan=lifespan)
app.include_router(health.router)


@app.get("/")
async def root():
    return {"status": "Active", "message": "Sovereign Agent Node Online"}


@app.post("/v1/agent/invoke", response_model=AgentResponse)
async def invoke_agent(payload: AgentRequest):
    # Simulated Agent Logic
    return AgentResponse(
        request_id=payload.request_id,
        status="processing",
        output=f"Agent '{payload.agent_id}' has received the task: {payload.task_description}"
    )
