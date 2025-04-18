from sim.schemas.github import (
    GitHubUser,
    Repository,
    PushEvent,
    IssueEvent,
    PullRequestEvent,
    ReleaseEvent
)
from sim.schemas.posthog import PostHogEvent, UsageMetricsData
from datetime import datetime

def github_examples():
    # Example repository data
    repo = Repository(
        id=123456789,
        name="awesome-project",
        full_name="octocat/awesome-project",
        private=False,
        description="An awesome project",
        language="Python"
    )

    # Example user data
    user = GitHubUser(
        id=1234567,
        login="octocat",
        type="User",
        avatar_url="https://github.com/images/octocat.png"
    )

    # Example push event
    push_event = PushEvent(
        ref="refs/heads/main",
        before="6dcb09b5b57875f334f61aebed695e2e4193db5e",
        after="76dcb09b5b57875f334f61aebed695e2e4193db5",
        commits=[
            {
                "id": "76dcb09b5b57875f334f61aebed695e2e4193db5",
                "message": "Fix bug in login system",
                "timestamp": "2024-03-15T15:00:00Z"
            }
        ],
        repository=repo,
        sender=user
    )

    # Example issue event
    issue_event = IssueEvent(
        action="opened",
        issue={
            "number": 123,
            "title": "Add new feature",
            "body": "We should add this cool new feature",
            "state": "open"
        },
        repository=repo,
        sender=user
    )

    print("GitHub Events Examples:")
    print("Push Event:", push_event.model_dump_json(indent=2))
    print("\nIssue Event:", issue_event.model_dump_json(indent=2))

def posthog_examples():
    # Example PostHog usage metrics event
    usage_metrics = PostHogEvent(
        source="posthog",
        event="usage.metrics",
        org_id="doestack",
        timestamp=datetime.fromisoformat("2025-04-17T14:00:00Z"),
        data=UsageMetricsData(
            active_users=102,
            previous_period=184,
            percent_change=-44.6
        )
    )

    print("\nPostHog Events Examples:")
    print("Usage Metrics Event:", usage_metrics.model_dump_json(indent=2))

def main():
    github_examples()
    posthog_examples()

if __name__ == "__main__":
    main() 