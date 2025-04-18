from datetime import datetime, timedelta
from typing import List, Iterator, Optional
from .sources import EventSource
from .events import BaseEvent

class EventStream:
    """
    Main class for configuring and running event simulations.
    
    Args:
        start_time: When to start generating events from
        duration: How long to generate events for
        seed: Optional random seed for reproducibility
    """
    def __init__(
        self,
        start_time: datetime,
        duration: timedelta,
        seed: Optional[int] = None
    ):
        self.start_time = start_time
        self.end_time = start_time + duration
        self.sources: List[EventSource] = []
        
        if seed is not None:
            import random
            random.seed(seed)
    
    def add_source(self, source: EventSource) -> None:
        """Add an event source to the stream."""
        self.sources.append(source)
    
    def run(self) -> Iterator[BaseEvent]:
        """
        Run the simulation and generate events.
        
        Yields:
            Events in chronological order from all sources.
        """
        # Initialize source contexts
        contexts = {source: {} for source in self.sources}
        
        # Current time pointer
        current_time = self.start_time
        
        while current_time <= self.end_time:
            # Get next event from each source
            for source in self.sources:
                event = source.generate_event(current_time, contexts[source])
                if event:
                    yield event
                    # Update source context
                    contexts[source] = source.update_context(event, contexts[source])
            
            # Move time forward
            current_time += timedelta(minutes=1)  # Can be configurable 