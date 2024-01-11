import json
import os
import requests

def debug_log(message):
    if os.getenv('RUNNER_DEBUG') or os.getenv('ACTIONS_STEP_DEBUG') or (os.getenv('ACTIONS_RUNNER_DEBUG', 'false').lower() == 'true'):
        print(message)

def main():
    # Define the path for the team secrets configuration
    config_path = os.getenv('INPUT_CONFIG_PATH') or os.getenv('NOTIFICATIONS_CONFIG_PATH') or 'team_secrets_config.json'

    # Load the event data
    event_path = os.getenv('GITHUB_EVENT_PATH')
    if not event_path or not os.path.exists(event_path):
        print("GitHub event path is missing or invalid.")
        return

    with open(event_path, 'r') as event_file:
        event = json.load(event_file)
        event_type = event.get('action', 'unknown event')

    debug_log(f"Event data: {event}")
    debug_log(f"Event type: {event_type}")

    # Extract relevant data based on the type of event
    comment_body, html_url = '', ''
    if 'comment' in event:
        comment_body = event['comment']['body']
        html_url = event['comment']['html_url']
    elif 'pull_request' in event:
        comment_body = event['pull_request']['body']
        html_url = event['pull_request']['html_url']
    elif 'issue' in event:
        comment_body = event['issue']['body']
        html_url = event['issue']['html_url']

    # Load the team secrets configuration
    if not os.path.exists(config_path):
        print(f"Configuration file not found at {config_path}.")
        return

    with open(config_path, 'r') as file:
        team_secrets = json.load(file)

    # Check for mentions, assignments, or review requests
    notification_sent = False
    for team_secret in team_secrets:
        org = team_secret['org']
        team_id = team_secret['team_id'].lower()
        webhook_secret_name = team_secret['webhook_secret_name']
        target_team_name = team_secret.get('target_team_name', f"@{org}/{team_id}")
        webhook_url = os.getenv(webhook_secret_name)
        mention_tag = f"@{org}/{team_id}"

        if not webhook_url:
            debug_log(f"No webhook URL found for {org}/{team_id} (secret {webhook_secret_name}).")
            continue

        # Check if the team is mentioned, assigned, or requested for review
        is_mentioned = mention_tag in comment_body
        debug_log(f"Checking for mentions of {mention_tag} in {comment_body}")

        assignees = event.get('assignees', [])
        debug_log(f"Checking for assignments of {mention_tag} in {assignees}")
        is_assigned = any(mention_tag in assignee['login'] for assignee in assignees)

        requested_teams = event['pull_request'].get('requested_teams', []) if 'pull_request' in event else []
        debug_log(f"Checking for review requests of {org}/{team_id} in {requested_teams}")
        team_pattern = f"https://github.com/{org}/teams/{team_id}"
        is_requested_for_review = any(team_pattern.lower() in team.get('html_url', '').lower() for team in requested_teams)

        if is_mentioned or is_assigned or is_requested_for_review:
            action = "mentioned" if is_mentioned else "assigned" if is_assigned else "requested for review"
            message = f"{target_team_name} {action} in GitHub ({event_type}): {html_url}"
            payload = {"text": message}
            response = requests.post(webhook_url, json=payload)
            if response.status_code == 200:
                print(f"Notification sent successfully to {target_team_name}")
                notification_sent = True
            else:
                print(f"Failed to send notification to {target_team_name}")
        else:
            debug_log(f"No mentions, assignments, or review requests of {target_team_name}({mention_tag}) found.")

    if not notification_sent:
        print("No relevant team mentions, assignments, or review requests found, no notifications sent.")

if __name__ == "__main__":
    main()
