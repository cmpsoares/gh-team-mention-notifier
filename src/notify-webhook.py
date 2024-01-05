import json
import os
import requests

# Load the event data
with open(os.getenv('GITHUB_EVENT_PATH'), 'r') as event_file:
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

# Load the notifications configuration
with open('notifications_config.json', 'r') as file:
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
