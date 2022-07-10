import asyncio
from telebot.async_telebot import AsyncTeleBot
import time
import os

from functions.send_help import send_help
import config.config as config

bot = AsyncTeleBot(config.bot_token,parse_mode='markdown')

bot.register_message_handler(send_help,commands=['start','help'],pass_bot=True)

asyncio.run(bot.infinity_polling())