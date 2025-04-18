from dataclasses import dataclass
from typing import Dict, List, Optional, Union
from datetime import datetime
from pydantic import BaseModel, Field

@dataclass
class Event:
    """Core event object that represents a single activity across any source."""
    source: str
    event: str
    org_id: str
    timestamp: str
    data: dict

    def __lt__(self, other):
        """Make Event comparable for priority queue."""
        if not isinstance(other, Event):
            return NotImplemented
        return self.timestamp < other.timestamp

class DataRule(BaseModel):
    """Represents a dynamic data generation rule."""
    type: str = Field(..., description="Type of rule (random, static, random_text)")
    args: List[Union[int, float, str]] = Field(default_factory=list)
    kwargs: Dict[str, Union[int, float, str]] = Field(default_factory=dict)

class EventSpec(BaseModel):
    """Specification for a single event type in a story."""
    source: str
    event: str
    offset_days: int = Field(ge=0)
    repeat: Optional[int] = Field(default=None, ge=0)
    data: Dict[str, Union[str, int, float, dict, list]] = Field(default_factory=dict)

class StoryConfig(BaseModel):
    """Top-level story configuration."""
    org_id: str
    start_date: datetime
    includes: Optional[List[str]] = None
    events: List[EventSpec]

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
