# GitHub Team Mention Notifier (gh-team-mention-notifier)

`gh-team-mention-notifier` is a GitHub Action designed to notify specified communication platforms via webhooks when a team is mentioned or assigned in issues, PRs, or comments. It's compatible with Slack, Microsoft Teams, and other webhook-enabled services.

## Features

- **Team Mention and Assignment Detection**: Detects mentions and assignments of teams in comments of issues, pull requests, and direct assignments.
- **Customizable Configuration**: Use a JSON file to map team mentions to webhook URLs.
- **Multiple Platform Support**: Compatible with any service that accepts incoming webhooks, including Slack and Microsoft Teams.
- **Dockerized for Consistency**: Runs in a Docker container for consistent testing and deployment environments.

## Getting Started

### Prerequisites

- A GitHub repository where you can set up Actions.
- Docker environment as the action runs in a Docker container.
- Webhook URLs from the platforms (Slack, Microsoft Teams, etc.) where you want to send notifications.

### Setup

#### 1. **Create and Configure the Configuration File**

Create a file named `notifications_config.json` in your repository with the following structure:

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

This file maps team mentions to the environment variable names for your webhook URLs.

#### 2. **Commit the Configuration File**

Commit the `notifications_config.json` file to your repository for the GitHub Action to access.

#### 3. **Set Up Secrets**

For each team, set up a secret in your repository settings containing the webhook URL. The secret name should correspond to the `webhook_secret_name` specified in your configuration file.

### Usage

In your GitHub workflow file (e.g., `.github/workflows/notify.yml`), configure the action as follows:

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
      uses: cmpsoares/gh-team-mention-notifier@v1.0.22
      with:
        config_path: 'notifications_config.json'
      env:
        TEAM1_WEBHOOK: ${{ secrets.TEAM1_WEBHOOK }}
        TEAM2_WEBHOOK: ${{ secrets.TEAM2_WEBHOOK }}
        # Add more environment variables as needed
```

### Using Organization-Level Configuration Variables

In scenarios where you need to use organization-level configuration variables with `gh-team-mention-notifier`, follow these steps to set up and reference these variables in your workflow:

#### Setting Up Organization-Level Variables

1. **Create Organization Variables**: Define your configuration variables at the organization level on GitHub. This could include variables like `ORG_NOTIFICATION_CONFIG` to store the JSON configuration for team mentions.

2. **Set Variable Visibility**: Ensure the variable is set with the appropriate visibility settings. You can choose to make it available to all repositories or select specific repositories within your organization.

#### Updating Workflow to Use Organization Variables

In your GitHub workflow file, update the steps to use the organization variable using the `vars` context. Here's an example:

```yaml
jobs:
  notification_job:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout
      uses: actions/checkout@v2

    - name: Setup Configuration
      run: |
        echo "$ORG_NOTIFICATION_CONFIG" > .github/workflows/notifications_config.json
      env:
        ORG_NOTIFICATION_CONFIG: ${{ vars.ORG_NOTIFICATION_CONFIG }}

    - name: Notify Teams
      uses: cmpsoares/gh-team-mention-notifier@latest
      with:
        config_path: '.github/workflows/notifications_config.json'
```

In this example, `ORG_NOTIFICATION_CONFIG` is an organization-level variable that contains the JSON configuration. The workflow writes this configuration to a file, which is then used by the `gh-team-mention-notifier` action.

#### Notes

- Make sure the organization variable `ORG_NOTIFICATION_CONFIG` is correctly set up and accessible to the repository where the workflow runs.
- This method is particularly useful for managing configuration centrally at the organization level, especially when the same configuration is shared across multiple repositories.

## Contributing

Contributions to `gh-team-mention-notifier` are welcome! Please feel free to report issues, suggest features, or submit pull requests.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

Thank you to all the contributors and users of `gh-team-mention-notifier`. Your support and feedback are greatly appreciated.
