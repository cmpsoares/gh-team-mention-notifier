# GH Team Mention Notifier (gh-team-mention-notifier)

A GitHub Action for notifying communication platforms via webhooks when a team is mentioned in issues, PRs, or comments. Compatible with Slack, Microsoft Teams, and other webhook-enabled services.

## Configuration

1. Copy `notifications_config.json.example` to `notifications_config.json`.
2. Fill in the real webhook URLs for your teams.

## Setting Up Secrets

Ensure you set up the following secrets in your GitHub repository:

- `GITHUB_TOKEN`: Your GitHub authentication token.

## Usage

Add a workflow file to your `.github/workflows` directory:

```yaml
name: Team Mention Notification
on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [submitted]
  pull_request:
    types: [opened, reopened]

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
      - name: Notify Teams
        run: python src/notify_webhook.py
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Contributing
Contributions are welcome! Please feel free to submit a pull request.