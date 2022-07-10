import asyncio
import telebot.async_telebot as telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def gen_markup(botton_list,row_width=2):
    markup = InlineKeyboardMarkup()
    markup.row_width = row_width
    for botton in botton_list:
        markup.add(InlineKeyboardButton(botton[0], callback_data=botton[1]))
    return markup