from pydantic import BaseModel, Field
from typing import List, Optional

class UsageMetricsSchema(BaseModel):
    """Schema for PostHog usage metrics events."""
    percent_change: float = Field(..., description="Percentage change in usage")
    active_users: int = Field(..., description="Number of active users")
    total_events: Optional[int] = Field(None, description="Total number of events tracked")
    retention_rate: Optional[float] = Field(None, description="User retention rate")

class FeatureUsageSchema(BaseModel):
    """Schema for PostHog feature usage events."""
    feature_id: str = Field(..., description="Unique identifier for the feature")
    name: str = Field(..., description="Feature name")
    usage_count: int = Field(..., description="Number of times feature was used")
    unique_users: int = Field(..., description="Number of unique users")

class UserActionSchema(BaseModel):
    """Schema for PostHog user action events."""
    user_id: str = Field(..., description="User identifier")
    action: str = Field(..., description="Action performed")
    properties: dict = Field(default_factory=dict, description="Action properties")
    session_id: Optional[str] = Field(None, description="Session identifier") 