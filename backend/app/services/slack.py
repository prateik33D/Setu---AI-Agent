from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import logging

logger = logging.getLogger(__name__)

class SlackService:
    """Slack operations"""

    def __init__(self, access_token: str):
        self.client = WebClient(token=access_token)

    def send_message(self, channel: str, text: str) -> dict:
        """Send message to a Slack channel"""
        try:
            # Normalize channel name
            if not channel.startswith('#') and not channel.startswith('C'):
                channel = f"#{channel}"

            response = self.client.chat_postMessage(
                channel=channel,
                text=text
            )

            return {
                "message_ts": response["ts"],
                "channel": response["channel"],
                "status": "sent"
            }
        except SlackApiError as e:
            logger.error(f"Slack error: {e.response['error']}")
            raise Exception(f"Slack send failed: {e.response['error']}")
        except Exception as e:
            logger.error(f"Failed to send Slack message: {e}")
            raise
