"""
Slack Standup Bot
Showcases: Workflow Builder API + Block Kit
"""
import os
from datetime import datetime
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()

client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")

def create_standup_message():
    """Create rich Block Kit message for standup."""
    today = datetime.now().strftime("%A, %B %d")

    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"Daily Standup - {today}",
                "emoji": True
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Good morning team! Time for our daily standup."
            }
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Please share your update:*"
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Yesterday:*\nWhat did you accomplish?"
                },
                {
                    "type": "mrkdwn",
                    "text": "*Today:*\nWhat will you work on?"
                }
            ]
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Blockers:*\nAnything blocking your progress?"
                },
                {
                    "type": "mrkdwn",
                    "text": "*Help Needed:*\nNeed assistance from anyone?"
                }
            ]
        },
        {"type": "divider"},
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Submit Update",
                        "emoji": True
                    },
                    "style": "primary",
                    "action_id": "submit_standup"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Skip Today",
                        "emoji": True
                    },
                    "action_id": "skip_standup"
                }
            ]
        }
    ]

    return blocks

def post_standup_prompt():
    """Post standup message to channel."""
    try:
        response = client.chat_postMessage(
            channel=CHANNEL_ID,
            blocks=create_standup_message(),
            text="Daily Standup Time!"  # Fallback
        )
        print(f"Posted standup message: {response['ts']}")
        return response
    except SlackApiError as e:
        print(f"Error posting message: {e.response['error']}")
        return None

def create_summary_message(updates: list):
    """Create summary of standup responses."""
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "Standup Summary",
                "emoji": True
            }
        },
        {"type": "divider"}
    ]

    for update in updates:
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*<@{update['user']}>*\n"
                        f"Yesterday: {update['yesterday']}\n"
                        f"Today: {update['today']}\n"
                        f"Blockers: {update.get('blockers', 'None')}"
            }
        })
        blocks.append({"type": "divider"})

    return blocks

def main():
    print("=" * 50)
    print("Slack Standup Bot")
    print("=" * 50)

    if not os.getenv("SLACK_BOT_TOKEN"):
        print("\nSetup required:")
        print("1. Create Slack App at https://api.slack.com/apps")
        print("2. Add Bot Token Scopes: chat:write, channels:read")
        print("3. Enable Workflow Steps (for Workflow Builder API)")
        print("4. Install to workspace and copy Bot Token")
        print("5. Add bot to target channel")
        return

    print("\nSlack Bot configured!")

    # Demo: Create standup message blocks
    print("\n📋 Standup Message Preview:")
    blocks = create_standup_message()
    print(f"  - {len(blocks)} Block Kit components")
    print("  - Interactive buttons included")

    # Demo: Summary message
    sample_updates = [
        {"user": "U123", "yesterday": "Finished API integration", "today": "Writing tests", "blockers": "None"},
        {"user": "U456", "yesterday": "Code review", "today": "Deploy to staging", "blockers": "Waiting on design"},
    ]

    print("\n📊 Summary Message Preview:")
    summary = create_summary_message(sample_updates)
    print(f"  - {len(sample_updates)} team member updates")

    # Uncomment to actually post
    # post_standup_prompt()

    print("\n💡 Workflow Builder Integration:")
    print("  1. Create workflow in Slack")
    print("  2. Add 'Custom Step' using this bot")
    print("  3. Schedule daily at 9:00 AM")
    print("  4. Collect responses and summarize")

if __name__ == "__main__":
    main()
