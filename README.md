# Autosource.sim - Event Simulation Engine for Pulse

A0-L1 simulation layer for Pulse that generates synthetic but realistic operational events for testing and development.

## Overview

Autosource.sim is a simulation-only implementation of the A0 layer that generates synthetic `Event` objects simulating real company activity across various operational tools (PostHog, Stripe, Linear, etc.).

## Features

- YAML-based stream definitions (stories)
- Multi-source event simulation
- Dynamic field generation with rule resolution
- Pydantic schema validation
- Chronological event ordering
- Story composition and reuse
- Tool-agnostic event generation

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from autosource.engine import stream_story

# Stream events from a story file
for event in stream_story("stories/example.yaml"):
    print(event)
```

## Story Format

Stories are defined in YAML with the following structure:

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

## Project Structure

- `autosource/`
  - `config.py`: Configuration models
  - `engine.py`: Main simulation engine
  - `rule_resolver.py`: Dynamic field resolution
  - `registry.py`: Event schema registry
  - `faker_utils.py`: Synthetic data utilities
  - `schemas/`: Event type schemas
  - `generators/`: Event data generators
  - `stories/`: Example story files

## License

MIT
