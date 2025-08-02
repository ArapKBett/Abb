import discord
from discord import Webhook, RequestsWebhookAdapter
import aiohttp
import asyncio
import logging

class DiscordNotifier:
    def __init__(self, webhook_url, channel_id, bot_token):
        self.webhook_url = webhook_url
        self.channel_id = channel_id
        self.bot_token = bot_token
        self.logger = logging.getLogger(__name__)
        self.client = discord.Client(intents=discord.Intents.default())

    async def send_message(self, message):
        try:
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(self.webhook_url, adapter=RequestsWebhookAdapter(session=session))
                await webhook.send(content=message)
        except Exception as e:
            self.logger.error(f"Failed to send Discord message: {e}")

    async def start_bot(self):
        try:
            await self.client.start(self.bot_token)
        except Exception as e:
            self.logger.error(f"Failed to start Discord bot: {e}")
