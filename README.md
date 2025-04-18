# AutoSourceSim

A simple Python library for simulating realistic event streams. Perfect for testing event-driven applications and data pipelines.

## Installation

```bash
pip install autosourcesim
```

## Quick Start

```python
from autosourcesim import EventStream, PostHogSource
from datetime import datetime, timedelta

# Configure your event stream
stream = EventStream(
    start_time=datetime.now(),
    duration=timedelta(hours=24)
)

# Add a PostHog source with rules
posthog = PostHogSource(
    org_id="my-company",
    rules={
        "usage.metrics": {
            "frequency": "1h",  # Generate every hour
            "data": {
                "active_users": lambda: random.randint(80, 200),
                "previous_period": lambda prev: prev.get("active_users", 100),
                "percent_change": lambda curr, prev: (curr["active_users"] - prev["active_users"]) / prev["active_users"] * 100
            }
        }
    }
)

# Add source to stream
stream.add_source(posthog)

# Generate events
for event in stream.run():
    print(event.model_dump_json())
```

## Features

- Simple, intuitive API for defining event streams
- Built-in support for common event sources (PostHog, GitHub, etc.)
- Rule-based event generation with realistic patterns
- Time-bound simulation with proper event ordering
- Extensible for custom event sources and rules

## Creating a Custom Source

```python
from autosourcesim import EventSource, BaseEvent
from pydantic import Field

class MyCustomEvent(BaseEvent):
    event_type: str
    user_id: str
    data: dict

class MyCustomSource(EventSource):
    def __init__(self, rules):
        super().__init__(name="custom", rules=rules)
    
    def generate_event(self, time, context):
        # Your event generation logic here
        return MyCustomEvent(...)

# Use it in your stream
custom_source = MyCustomSource(rules={...})
stream.add_source(custom_source)
```

## Documentation

For more examples and detailed documentation, visit [our documentation](https://github.com/yourusername/autosourcesim).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 