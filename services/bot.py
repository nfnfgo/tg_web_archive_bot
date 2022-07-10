from telebot.async_telebot import AsyncTeleBot
import asyncio

import config

bot = AsyncTeleBot(config.bot_token)