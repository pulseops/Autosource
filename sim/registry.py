from typing import Dict, Type, Tuple
from pydantic import BaseModel

from .schemas.common import (
    AnalyticsEvent,
    MetricsEvent,
    AlertEvent,
    TransactionEvent,
    UserEvent
)

class EventRegistry:
    """Registry mapping event types to their schemas."""
    
    def __init__(self):
        self._schemas: Dict[Tuple[str, str], Type[BaseModel]] = {}
        self._register_schemas()
    
    def _register_schemas(self):
        """Register all available event schemas."""
        # Analytics events
        self._schemas[("analytics", "page.view")] = AnalyticsEvent
        self._schemas[("analytics", "search.performed")] = AnalyticsEvent
        self._schemas[("analytics", "feature.usage")] = AnalyticsEvent
        self._schemas[("analytics", "user.signup")] = UserEvent
        
        # Monitoring events
        self._schemas[("monitoring", "system.metrics")] = MetricsEvent
        self._schemas[("monitoring", "system.alert")] = AlertEvent
        self._schemas[("monitoring", "error.occurred")] = AlertEvent
        self._schemas[("monitoring", "db.connections")] = MetricsEvent
        
        # Business events
        self._schemas[("payment", "transaction.created")] = TransactionEvent
        self._schemas[("inventory", "stock.updated")] = MetricsEvent
        self._schemas[("shipping", "shipment.created")] = TransactionEvent
    
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
