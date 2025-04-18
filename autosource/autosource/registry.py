from typing import Dict, Type, Tuple
from pydantic import BaseModel

from .schemas.posthog import (
    UsageMetricsSchema,
    FeatureUsageSchema,
    UserActionSchema
)
from .schemas.linear import (
    TicketSchema,
    CommentSchema,
    WorkflowStateSchema
)

class EventRegistry:
    """Registry mapping event types to their schemas and generators."""
    
    def __init__(self):
        self._schemas: Dict[Tuple[str, str], Type[BaseModel]] = {}
        self._register_schemas()
    
    def _register_schemas(self):
        """Register all available event schemas."""
        # PostHog events
        self._schemas[("posthog", "usage.metrics")] = UsageMetricsSchema
        self._schemas[("posthog", "feature.usage")] = FeatureUsageSchema
        self._schemas[("posthog", "user.action")] = UserActionSchema
        
        # Linear events
        self._schemas[("linear", "ticket.created")] = TicketSchema
        self._schemas[("linear", "ticket.updated")] = TicketSchema
        self._schemas[("linear", "comment.created")] = CommentSchema
        self._schemas[("linear", "workflow.state_changed")] = WorkflowStateSchema
    
    def get_schema(self, source: str, event: str) -> Type[BaseModel]:
        """Get the schema for a given event type."""
        key = (source, event)
        if key not in self._schemas:
            raise ValueError(f"No schema registered for event: {source}.{event}")
        return self._schemas[key]
    
    def validate_data(self, source: str, event: str, data: dict) -> dict:
        """Validate event data against its schema."""
        schema = self.get_schema(source, event)
        validated = schema(**data)
        return validated.model_dump()
    
    def list_events(self) -> list[Tuple[str, str]]:
        """List all registered event types."""
        return list(self._schemas.keys())

# Global registry instance
_REGISTRY: EventRegistry = None

def get_registry() -> EventRegistry:
    """Get or create the global registry instance."""
    global _REGISTRY
    if _REGISTRY is None:
        _REGISTRY = EventRegistry()
    return _REGISTRY
