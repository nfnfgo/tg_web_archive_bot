import asyncio
import aiohttp
from telebot.async_telebot import AsyncTeleBot


bot = AsyncTeleBot(config.bot_token)

# send help function
async def send_help(message):
    