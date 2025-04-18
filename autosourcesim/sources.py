from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from .events import BaseEvent

class EventSource(ABC):
    """
    Base class for event sources.
    
    Args:
        name: Name of the source
        rules: Dictionary of rules for event generation
    """
    def __init__(self, name: str, rules: Dict[str, Any]):
        self.name = name
        self.rules = rules
    
    @abstractmethod
    def generate_event(self, time: datetime, context: Dict) -> Optional[BaseEvent]:
        """Generate the next event at the given time."""
        pass
    
    def update_context(self, event: BaseEvent, context: Dict) -> Dict:
        """Update source context after generating an event."""
        return context

class PostHogEvent(BaseEvent):
    """PostHog specific event."""
    org_id: str = Field(..., description="Organization ID")
    data: Dict[str, Any] = Field(..., description="Event data")

class PostHogSource(EventSource):
    """PostHog event source."""
    def __init__(self, org_id: str, rules: Dict[str, Any]):
        super().__init__("posthog", rules)
        self.org_id = org_id
    
    def generate_event(self, time: datetime, context: Dict) -> Optional[BaseEvent]:
        for event_type, rule in self.rules.items():
            # Check if we should generate an event based on frequency
            if self._should_generate(time, rule.get("frequency", "1h"), context):
                # Generate event data using rule functions
                data = {}
                for field, func in rule["data"].items():
                    if callable(func):
                        data[field] = func(context.get("prev_data", {}))
                
                return PostHogEvent(
                    source=self.name,
                    event_type=event_type,
                    timestamp=time,
                    org_id=self.org_id,
                    data=data
                )
        return None
    
    def update_context(self, event: BaseEvent, context: Dict) -> Dict:
        context["prev_data"] = event.data
        return context
    
    def _should_generate(self, time: datetime, frequency: str, context: Dict) -> bool:
        """Determine if we should generate an event based on frequency."""
        if frequency.endswith('h'):
            return time.minute == 0
        elif frequency.endswith('m'):
            return True
        return False

class GitHubEvent(BaseEvent):
    """GitHub specific event."""
    repo: str = Field(..., description="Repository name")
    actor: str = Field(..., description="GitHub username")
    data: Dict[str, Any] = Field(..., description="Event data")

class GitHubSource(EventSource):
    """GitHub event source."""
    def __init__(self, repos: List[str], actors: List[str], rules: Dict[str, Any]):
        super().__init__("github", rules)
        self.repos = repos
        self.actors = actors
    
    def generate_event(self, time: datetime, context: Dict) -> Optional[BaseEvent]:
        import random
        
        for event_type, rule in self.rules.items():
            if self._should_generate(time, rule.get("probability", 0.1)):
                return GitHubEvent(
                    source=self.name,
                    event_type=event_type,
                    timestamp=time,
                    repo=random.choice(self.repos),
                    actor=random.choice(self.actors),
                    data=rule["template"].copy()  # Use template with potential randomization
                )
        return None
    
    def _should_generate(self, time: datetime, probability: float) -> bool:
        import random
        return random.random() < probability 