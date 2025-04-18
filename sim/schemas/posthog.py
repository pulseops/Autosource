from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UsageMetricsData(BaseModel):
    active_users: int = Field(..., description="Number of active users in the current period")
    previous_period: int = Field(..., description="Number of active users in the previous period")
    percent_change: float = Field(..., description="Percentage change in active users")

class PostHogEvent(BaseModel):
    source: str = Field(..., description="Source of the event, e.g., 'posthog'")
    event: str = Field(..., description="Type of event, e.g., 'usage.metrics'")
    org_id: str = Field(..., description="Organization identifier")
    timestamp: datetime = Field(..., description="Timestamp when the event occurred")
    data: UsageMetricsData = Field(..., description="Event-specific data payload") 