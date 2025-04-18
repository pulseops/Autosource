import yaml
from typing import Generator, List
from datetime import datetime, timedelta
import heapq
from pathlib import Path

from .config import Event, StoryConfig, EventSpec
from .registry import get_registry
from .rule_resolver import RuleResolver

class SimulationEngine:
    """Main simulation engine that generates events from stories."""
    
    def __init__(self):
        self.registry = get_registry()
        self.rule_resolver = RuleResolver()
        self.processed_stories = set()
    
    def _load_story(self, path: str) -> StoryConfig:
        """Load and parse a story file."""
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
            if isinstance(data['start_date'], str):
                data['start_date'] = datetime.fromisoformat(data['start_date'])
        return StoryConfig(**data)
    
    def _resolve_includes(self, story: StoryConfig, base_path: Path) -> List[EventSpec]:
        """Resolve and merge included stories."""
        all_events = list(story.events)
        
        if story.includes:
            for include in story.includes:
                include_path = (base_path / include).resolve()
                if str(include_path) in self.processed_stories:
                    continue
                    
                self.processed_stories.add(str(include_path))
                included_story = self._load_story(str(include_path))
                all_events.extend(self._resolve_includes(included_story, include_path.parent))
        
        return all_events
    
    def _generate_events(self, story: StoryConfig, events: List[EventSpec]) -> Generator[Event, None, None]:
        """Generate events from event specifications."""
        # Priority queue to maintain chronological order
        event_queue = []
        
        for event_spec in events:
            # Handle repeated events
            repeat_count = event_spec.repeat or 1
            for i in range(repeat_count):
                offset = event_spec.offset_days + (i * (1 if event_spec.repeat else 0))
                timestamp = story.start_date + timedelta(days=offset)
                
                # Resolve dynamic data fields
                data = self.rule_resolver.resolve_data(event_spec.data)
                
                # Validate against schema
                validated_data = self.registry.validate_data(
                    event_spec.source,
                    event_spec.event,
                    data
                )
                
                # Create event and add to queue
                event = Event(
                    source=event_spec.source,
                    event=event_spec.event,
                    org_id=story.org_id,
                    timestamp=timestamp.isoformat(),
                    data=validated_data
                )
                
                heapq.heappush(event_queue, event)
        
        # Yield events in chronological order
        while event_queue:
            yield heapq.heappop(event_queue)
    
    def stream_story(self, path: str) -> Generator[Event, None, None]:
        """Stream events from a story file."""
        story_path = Path(path)
        story = self._load_story(str(story_path))
        
        # Reset processed stories for this stream
        self.processed_stories = {str(story_path.resolve())}
        
        # Resolve includes and get all events
        all_events = self._resolve_includes(story, story_path.parent)
        
        # Generate and yield events
        yield from self._generate_events(story, all_events)

def stream_story(path: str) -> Generator[Event, None, None]:
    """Convenience function to stream events from a story file."""
    engine = SimulationEngine()
    yield from engine.stream_story(path) 