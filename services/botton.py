import asyncio
import telebot.async_telebot as telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, BotCommand,CallbackQuery


def gen_markup(botton_list, row_width=2):
    markup = InlineKeyboardMarkup()
    markup.row_width = row_width
    for botton in botton_list:
        markup.add(InlineKeyboardButton(botton[0], callback_data=botton[1]))
    return markup

# delete a markup of a message (unavailable when message is too old)


async def del_botton(call:CallbackQuery,bot):
    await bot.edit_message_reply_markup(call.message.chat.id,call.message.message_id,'')