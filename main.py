import asyncio
from email import message
from telebot.async_telebot import AsyncTeleBot
import time
import os

from functions import send_help
from functions import archive

import config.config as config

bot = AsyncTeleBot(config.bot_token, parse_mode='markdown')

# Welcome function
bot.register_message_handler(send_help.send_help, commands=['start', 'help'], pass_bot=True)
# check update botton callback
bot.register_callback_query_handler(send_help.get_update, func=lambda query: query.data == 'check_update', pass_bot=True)

# archive url funciton
bot.register_message_handler(archive.archive_url, commands=['archive','save','a','s'],pass_bot=True)

# catch all message
bot.register_message_handler(archive.archive_url_from_text, content_types=['text'], pass_bot=True)
# 二次确认 cbq
bot.register_callback_query_handler(archive.cbq_confirm_archive, func=lambda query: query.data in ['archive_continue_archive','archive_stop_archive'], pass_bot=True)

asyncio.run(bot.infinity_polling())