import aiohttp
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


class DiscordService:
    """Discord operations via Bot API"""

    BASE_URL = "https://discord.com/api/v10"

    def __init__(self, bot_token: str = None):
        self.bot_token = bot_token or settings.DISCORD_BOT_TOKEN
        if not self.bot_token:
            raise Exception("Discord bot token not configured")

    async def send_message(self, channel_id: str, content: str) -> dict:
        """Send a message to a Discord channel by channel ID"""
        try:
            url = f"{self.BASE_URL}/channels/{channel_id}/messages"
            headers = {
                "Authorization": f"Bot {self.bot_token}",
                "Content-Type": "application/json",
            }
            payload = {"content": content}

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as resp:
                    if resp.status == 200 or resp.status == 201:
                        data = await resp.json()
                        logger.info(f"Discord message sent to channel {channel_id}")
                        return {
                            "message_id": data["id"],
                            "channel_id": data["channel_id"],
                            "status": "sent",
                        }
                    else:
                        error = await resp.text()
                        logger.error(f"Discord API error ({resp.status}): {error}")
                        raise Exception(f"Discord send failed ({resp.status}): {error}")
        except aiohttp.ClientError as e:
            logger.error(f"Discord connection error: {e}")
            raise Exception(f"Discord connection failed: {e}")

    async def send_webhook_message(self, content: str, username: str = "Setu Agent") -> dict:
        """Send a message via Discord webhook (no bot token needed)"""
        webhook_url = settings.DISCORD_WEBHOOK_URL
        if not webhook_url or webhook_url == "your-discord-webhook-url":
            raise Exception("Discord webhook URL not configured. Set DISCORD_WEBHOOK_URL in .env")

        try:
            payload = {"content": content, "username": username}

            async with aiohttp.ClientSession() as session:
                async with session.post(webhook_url, json=payload) as resp:
                    if resp.status == 204 or resp.status == 200:
                        logger.info("Discord webhook message sent")
                        return {"status": "sent", "method": "webhook"}
                    else:
                        error = await resp.text()
                        logger.error(f"Discord webhook error ({resp.status}): {error}")
                        raise Exception(f"Discord webhook failed ({resp.status}): {error}")
        except aiohttp.ClientError as e:
            logger.error(f"Discord webhook connection error: {e}")
            raise Exception(f"Discord webhook connection failed: {e}")
