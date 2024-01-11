# GitHub Team Mention Notifier (gh-team-mention-notifier)

`gh-team-mention-notifier` is a GitHub Action designed to notify specified communication platforms via webhooks when a team is mentioned or assigned in issues, PRs, or comments. It's compatible with Slack, Microsoft Teams, and other webhook-enabled services.

## Features

- **Team Mention and Assignment Detection**: Detects mentions and assignments of teams in comments of issues, pull requests, and direct assignments.
- **Dynamic Configuration**: Custom configuration allows for dynamic mapping of team mentions to webhook URLs via environment variables.
- **Multiple Platform Support**: Compatible with any service that accepts incoming webhooks.
- **Dockerized for Consistency**: Runs in a Docker container for consistent testing and deployment environments.

## Getting Started

### Prerequisites

- A GitHub repository where you can set up Actions.
- Docker environment as the action runs in a Docker container.
- Webhook URLs from the platforms (Slack, Microsoft Teams, etc.) where you want to send notifications.

### Setup

#### 1. **Create and Configure the Configuration File**

Duplicate the `notifications_config.json.example` file and rename it to `notifications_config.json`. Fill in the mappings of your team mentions to the environment variable names for your webhook URLs. Optionally, include a different target team name for the webhook message.

```json
[
    {
        "org": "github_org",
        "team_id": "team1",
        "webhook_secret_name": "TEAM1_WEBHOOK",
        "target_team_name": "@DifferentNameInTargetSystem"
    },
    {
        "org": "github_org",
        "team_id": "team2",
        "webhook_secret_name": "TEAM2_WEBHOOK"
    }
    // Add more team mappings as needed
]
```

This file will be used by the GitHub Action to determine which webhook URLs (stored as secrets) correspond to which team mentions.

#### 2. **Commit the Configuration File**

Commit the `notifications_config.json` file to your repository so the GitHub Action can access it. As this file contains only references to the secrets and not the actual webhook URLs, it's safe to commit.

#### 3. **Set Up Secrets**

For each team, set up a secret in your repository settings containing the webhook URL. The secret name should match the `webhook_secret_name` you've provided in `notifications_config.json`.

### Usage

In your GitHub workflow file (e.g., `.github/workflows/notify.yml`), use the action like this:

```yaml
name: Team Mention Notification
on:
  issue_comment:
    types: [created, edited]
  pull_request_review_comment:
    types: [submitted, edited]
  pull_request:
    types: [opened, reopened, assigned, edited, synchronize]
  issues:
    types: [opened, assigned, edited]

jobs:
  notification_job:
    runs-on: ubuntu-latest
    name: Notify when team mentioned or assigned
    steps:
    - name: Checkout
      uses: actions/checkout@v2
    - name: Notify Teams
      uses: cmpsoares/gh-team-mention-notifier@v1.0.7
      with:
        config_path: 'notifications_config.json'
      env:
        TEAM1_WEBHOOK: ${{ secrets.TEAM1_WEBHOOK }}
        TEAM2_WEBHOOK: ${{ secrets.TEAM2_WEBHOOK }}
        # Add more environment variables as needed
```

## Contributing

Contributions to `gh-team-mention-notifier` are welcome! Please feel free to report issues, suggest features, or submit pull requests.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

Thank you to all the contributors and users of `gh-team-mention-notifier`. Your support and feedback are greatly appreciated.
