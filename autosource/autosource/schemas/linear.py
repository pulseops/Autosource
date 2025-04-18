from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class TicketSchema(BaseModel):
    """Schema for Linear ticket events."""
    title: str = Field(..., description="Ticket title")
    description: Optional[str] = Field(None, description="Ticket description")
    status: str = Field(default="backlog", description="Ticket status")
    priority: Optional[int] = Field(None, description="Ticket priority (0-4)")
    assignee: Optional[str] = Field(None, description="Assigned user ID")
    tags: List[str] = Field(default_factory=list, description="Ticket tags")
    team_id: Optional[str] = Field(None, description="Team identifier")

class CommentSchema(BaseModel):
    """Schema for Linear comment events."""
    ticket_id: str = Field(..., description="Associated ticket ID")
    body: str = Field(..., description="Comment content")
    user_id: str = Field(..., description="User who created the comment")
    mentions: List[str] = Field(default_factory=list, description="Mentioned user IDs")

class WorkflowStateSchema(BaseModel):
    """Schema for Linear workflow state events."""
    ticket_id: str = Field(..., description="Ticket identifier")
    from_state: str = Field(..., description="Previous state")
    to_state: str = Field(..., description="New state")
    changed_by: str = Field(..., description="User who changed the state")
    duration_in_state: Optional[int] = Field(None, description="Time spent in previous state (seconds)") 