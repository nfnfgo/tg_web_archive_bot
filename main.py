import asyncio
from telebot.async_telebot import AsyncTeleBot
import time
import os

import functions as func
import config.config as config

bot = AsyncTeleBot(config.bot_token)

@bot.message_handler(commands=['start','help'])
async def send_help():
    await func.send_help()

asyncio.run(bot.infinity_polling())