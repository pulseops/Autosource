import random
from datetime import datetime, timedelta
from autosourcesim import EventStream, PostHogSource, GitHubSource

def main():
    # Create a stream for the next 24 hours
    stream = EventStream(
        start_time=datetime.now(),
        duration=timedelta(hours=24),
        seed=42  # For reproducibility
    )

    # Add PostHog source
    posthog = PostHogSource(
        org_id="demo-company",
        rules={
            "usage.metrics": {
                "frequency": "1h",
                "data": {
                    "active_users": lambda _: random.randint(80, 200),
                    "previous_period": lambda prev: prev.get("active_users", 100),
                    "percent_change": lambda curr, prev: (
                        (curr["active_users"] - prev.get("active_users", 100))
                        / prev.get("active_users", 100)
                        * 100
                    )
                }
            }
        }
    )

    # Add GitHub source
    github = GitHubSource(
        repos=["demo/repo1", "demo/repo2"],
        actors=["user1", "user2", "user3"],
        rules={
            "push": {
                "probability": 0.1,  # 10% chance each minute
                "template": {
                    "branch": "main",
                    "commits": [{"message": "Update documentation"}]
                }
            },
            "pull_request": {
                "probability": 0.05,  # 5% chance each minute
                "template": {
                    "action": "opened",
                    "title": "Feature implementation"
                }
            }
        }
    )

    # Add sources to stream
    stream.add_source(posthog)
    stream.add_source(github)

    # Generate and print events
    for event in stream.run():
        print(f"{event.timestamp}: {event.source} - {event.event_type}")
        print(event.model_dump_json(indent=2))
        print("-" * 80)

if __name__ == "__main__":
    main() 