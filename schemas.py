from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime


class AgentRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    request_id: UUID = Field(default_factory=uuid4,
                             description="Unique identifier for the agentic trace")
    task_description: str = Field(..., min_length=10, max_length=500,
                                  example="Analyze the 2025 Q4 earnings report.")
    agent_id: str = Field(..., pattern=r"^[a-zA-Z0-9_-]+$",
                          description="Slug for the specific agent to invoke")
    priority: int = Field(default=1, ge=1, le=5,
                          description="Task priority from 1 (low) to 5 (high)")
    metadata: Optional[dict] = Field(
        default=None, description="Optional context or flags for the agent")


class AgentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    request_id: UUID
    status: str = Field(..., example="completed")
    output: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
