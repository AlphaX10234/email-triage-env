from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from enum import Enum


class Priority(str, Enum):
    URGENT = "urgent"
    HIGH = "high"
    NORMAL = "normal"
    LOW = "low"
    SPAM = "spam"


class Category(str, Enum):
    CUSTOMER_COMPLAINT = "customer_complaint"
    BILLING = "billing"
    TECHNICAL_SUPPORT = "technical_support"
    GENERAL_INQUIRY = "general_inquiry"
    SPAM = "spam"
    INTERNAL = "internal"
    SALES = "sales"
    LEGAL = "legal"


class Email(BaseModel):
    id: str
    subject: str
    sender: str
    body: str
    received_at: str
    has_attachment: bool = False
    thread_length: int = 1


class Observation(BaseModel):
    """What the agent sees at each step."""
    email: Email
    inbox_size: int = Field(..., description="Total emails remaining in inbox")
    step_number: int = Field(..., description="Current step in the episode")
    max_steps: int = Field(..., description="Maximum steps in the episode")
    previous_action: Optional[dict] = Field(None, description="Last action taken")
    task_id: str = Field(..., description="Which task is being evaluated")
    context: Optional[str] = Field(None, description="Additional context for the task")


class Action(BaseModel):
    """What the agent can do with an email."""
    priority: Priority = Field(..., description="Assign priority to the email")
    category: Category = Field(..., description="Categorize the email")
    action: Literal["reply", "forward", "archive", "delete", "escalate", "flag"] = Field(
        ..., description="Action to take on the email"
    )
    assign_to: Optional[str] = Field(None, description="Team/person to assign to (for forward/escalate)")
    reply_draft: Optional[str] = Field(None, description="Draft reply text (for reply action)")
    reason: Optional[str] = Field(None, description="Reason for the decision")


class Reward(BaseModel):
    """Reward signal after each action."""
    score: float = Field(..., ge=0.0, le=1.0, description="Step reward (0.0–1.0)")
    priority_correct: bool = Field(..., description="Was priority correctly assigned?")
    category_correct: bool = Field(..., description="Was category correctly assigned?")
    action_appropriate: bool = Field(..., description="Was the action appropriate?")
    partial_credit: float = Field(0.0, description="Partial credit awarded")
    feedback: str = Field(..., description="Human-readable feedback on the action")
    cumulative_score: float = Field(..., description="Running total score for the episode")
