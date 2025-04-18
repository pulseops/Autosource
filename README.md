# AutoSource

A powerful Python library for simulating realistic event streams, perfect for testing event-driven applications and data pipelines. AutoSource provides a flexible, YAML-based configuration system for generating synthetic but realistic operational events.

## 🚀 Features

- **YAML-based Stream Definitions**: Define complex event patterns using simple YAML stories
- **Multi-source Event Simulation**: Support for various data sources (PostHog, Stripe, Linear, etc.)
- **Dynamic Field Generation**: Powerful rule resolution for realistic data patterns
- **Time-based Simulation**: Precise control over event timing and sequences
- **Schema Validation**: Built-in Pydantic validation for type safety
- **Extensible Architecture**: Easy creation of custom event sources and generators

## 📦 Installation

```bash
pip install git+https://github.com/yourusername/autosource.git
```

## 🚀 Quick Start

```python
from autosource import stream_story

# Stream events from a story file
for event in stream_story("stories/example.yaml"):
    print(event)
```

### Example Story Definition

```yaml
org_id: doestack
start_date: 2025-04-01

events:
  - source: posthog
    event: usage.metrics
    offset_days: 0
    repeat: 7
    data:
      percent_change: random(-10, -5)
      active_users: random(80, 120)
```

## 📚 Documentation

### Project Structure
```
autosource/
├── sim/              # Core simulation engine
│   ├── engine.py     # Main simulation logic
│   ├── schemas/      # Event type definitions
│   └── generators/   # Data generators
├── stories/          # Example story files
└── tests/            # Test suite
```

### Available Event Sources

- **PostHog**: User analytics and metrics
- **Stripe**: Payment and subscription events
- **Linear**: Project management activities
- **Custom Sources**: Easily extend with your own sources

### Creating a Custom Source

```python
from autosource import EventSource, BaseEvent
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
```

## 📖 Detailed Documentation

For comprehensive documentation and examples, visit:
- [Simulation Guide](sim/README.md) - Detailed guide for event simulation
- [Example Stories](stories/) - Sample story configurations
- [API Reference](docs/API.md) - Complete API documentation

## 🛠️ Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/autosource.git
```

2. Install development dependencies:
```bash
pip install -e ".[dev]"
```

3. Run tests:
```bash
pytest
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT 