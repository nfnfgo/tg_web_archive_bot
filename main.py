import asyncio
from email import message
from telebot.async_telebot import AsyncTeleBot
import time
import os

from functions import send_help
import config.config as config

bot = AsyncTeleBot(config.bot_token, parse_mode='markdown')
# Welcome function
bot.register_message_handler(send_help.send_help, commands=['start', 'help'], pass_bot=True)
# check update botton callback
bot.register_callback_query_handler(send_help.get_update, func=lambda query: query.data == 'check_update', pass_bot=True)

asyncio.run(bot.infinity_polling())