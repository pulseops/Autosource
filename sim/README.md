# AutoSource Simulation Engine

The core simulation engine that powers AutoSource's event generation capabilities. This module handles the generation of synthetic but realistic operational events for testing and development.

## 🔍 Overview

The simulation engine is responsible for:
- Processing YAML story definitions
- Managing event timing and sequencing
- Resolving dynamic field values
- Ensuring data consistency across events
- Validating event schemas

## 🛠️ Core Components

### Story Engine
- Processes YAML story definitions
- Manages event sequencing and timing
- Handles story composition and reuse

### Rule Resolver
- Evaluates dynamic field expressions
- Maintains context between events
- Supports various data generation patterns

### Schema Registry
- Validates event structures
- Manages Pydantic models
- Ensures type safety

## 📝 Story Format Reference

Stories are defined in YAML with the following structure:

```yaml
# Basic Story Structure
org_id: string           # Organization identifier
start_date: date        # Simulation start date
end_date: date         # Optional: Simulation end date
timezone: string       # Optional: Default UTC

# Event Definitions
events:
  - source: string     # Event source (e.g., posthog, stripe)
    event: string     # Event type
    offset_days: int  # Days from start_date
    repeat: int      # Optional: Number of repetitions
    frequency: string # Optional: Repeat frequency (hourly, daily)
    data:           # Event-specific data
      field1: value
      field2: expression
```

### Dynamic Field Types

```yaml
# Available Field Generators
data:
  # Random Numbers
  value1: random(min, max)
  value2: gaussian(mean, stddev)
  
  # Time-based Values
  timestamp: datetime(format)
  interval: duration(hours=1)
  
  # Text and IDs
  user_id: uuid4()
  name: faker.name()
  
  # Contextual Values
  reference: prev.field_name
  computed: "template ${value}"
```

## 🔧 Usage Examples

### Basic Event Stream

```python
from autosource.sim import stream_story

# Stream events from a story file
for event in stream_story("stories/basic.yaml"):
    process_event(event)
```

### Custom Event Generation

```python
from autosource.sim import EventGenerator

class CustomGenerator(EventGenerator):
    def generate(self, context):
        # Custom generation logic
        return {
            "field1": self.resolve_value("expression"),
            "field2": self.get_context_value("prev.field")
        }
```

### Advanced Story Configuration

```yaml
# Complex Event Pattern
org_id: example_org
start_date: 2025-01-01
timezone: UTC

events:
  - source: posthog
    event: user.signup
    offset_days: 0
    repeat: 30
    frequency: daily
    data:
      user_id: uuid4()
      plan: choice(['free', 'pro', 'enterprise'])
      source: weighted({'google': 0.6, 'direct': 0.3, 'referral': 0.1})

  - source: stripe
    event: subscription.created
    offset_days: 0
    repeat: 30
    data:
      customer_id: ref(user.signup.user_id)
      plan: ref(user.signup.plan)
      amount: switch(plan, {
        'free': 0,
        'pro': 99,
        'enterprise': 499
      })
```

## 🔍 Debugging

Enable debug logging for detailed insight into the simulation process:

```python
import logging
logging.getLogger('autosource.sim').setLevel(logging.DEBUG)
```

## 📚 Further Reading

- [Event Source Reference](../docs/sources.md)
- [Field Generator Guide](../docs/generators.md)
- [Story Composition](../docs/stories.md)
