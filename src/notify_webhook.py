import json
import os
import requests

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

    # Check for mentions or assignments
    notification_sent = False
    for team in team_secrets:
        org = team['org']
        team_id = team['team_id'].lower()
        webhook_secret_name = team['webhook_secret_name']
        target_team_name = team.get('target_team_name', f"@{team_id}")
        webhook_url = os.getenv(webhook_secret_name)
        mention_tag = f"@{org}/{team_id}"

        if not webhook_url:
            print(f"No webhook URL found for {org}/{team_id} (secret {webhook_secret_name}).")
            continue

        # Check if the team is mentioned in the comment body or assigned
        is_mentioned = mention_tag in comment_body
        is_assigned = any(mention_tag in assignee['login'] for assignee in event.get('assignees', []))

        if is_mentioned or is_assigned:
            action = "mentioned" if is_mentioned else "assigned"
            message = f"{target_team_name} {action} in GitHub: {html_url}"
            payload = {"text": message}
            response = requests.post(webhook_url, json=payload)
            if response.status_code == 200:
                print(f"Notification sent successfully to {target_team_name}")
                notification_sent = True
            else:
                print(f"Failed to send notification to {target_team_name}")
        else:
            print(f"No mentions or assignments of {target_team_name}({mention_tag}) found.")

    if not notification_sent:
        print("No relevant team mentions or assignments found, no notifications sent.")

if __name__ == "__main__":
    main()
