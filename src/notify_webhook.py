import json
import os
import requests

def main():
    # Define the default config path
    default_config_path = 'notifications_config.json'
    
    # Check for the action input first, fall back to the original environment variable,
    # and then to the default path if neither is provided
    config_path = os.getenv('INPUT_CONFIG_PATH') or os.getenv('NOTIFICATIONS_CONFIG_PATH') or default_config_path

    # Load the event data
    event_path = os.getenv('GITHUB_EVENT_PATH')
    if not event_path or not os.path.exists(event_path):
        print("GitHub event path is missing or invalid.")
        return

    with open(event_path, 'r') as event_file:
        event = json.load(event_file)

    # Extract relevant data based on the type of event
    comment_body = ''
    html_url = ''
    if 'comment' in event:
        comment_body = event['comment']['body']
        html_url = event['comment']['html_url']
    elif 'pull_request' in event:
        comment_body = event['pull_request']['body']
        html_url = event['pull_request']['html_url']

    # Check if the configuration file exists
    if not os.path.exists(config_path):
        print(f"Configuration file not found at {config_path}.")
        return

    # Load the notifications configuration
    with open(config_path, 'r') as file:
        webhooks = json.load(file)

    # Send notification if the team is mentioned
    for team_mention, webhook_url in webhooks.items():
        if team_mention in comment_body:
            payload = {"text": f"Team {team_mention} mentioned in GitHub: {html_url}"}
            response = requests.post(webhook_url, json=payload)
            if response.status_code == 200:
                print(f"Notification sent successfully to {team_mention}")
            else:
                print(f"Failed to send notification to {team_mention}")

if __name__ == "__main__":
    main()
