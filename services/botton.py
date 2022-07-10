import asyncio
import telebot.async_telebot as telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def gen_markup(row_width, botton_list):
    markup = InlineKeyboardMarkup()
    markup.row_width = row_width
    for botton in botton_list:
        markup.add(InlineKeyboardButton(botton[0], callback_data=botton[1]))
    return markup