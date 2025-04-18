from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any

class BaseEvent(BaseModel):
    """Base class for all events in the system."""
    source: str = Field(..., description="Source system that generated the event")
    event_type: str = Field(..., description="Type of event")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

    def get_source_name(self) -> str:
        """Get the canonical name of the event source."""
        return self.source.lower()

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        } 