import asyncio
import telebot.async_telebot as telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, BotCommand,CallbackQuery


def gen_markup(botton_list, row_width=2):
    buttons = []
    markup=InlineKeyboardMarkup()
    for i in botton_list:
        button = InlineKeyboardButton(i[0], callback_data=i[1])
        buttons.append(button)
    markup.add(*buttons)
    return markup

# delete a markup of a message (unavailable when message is too old)


async def del_botton(call:CallbackQuery,bot):
    await bot.edit_message_reply_markup(call.message.chat.id,call.message.message_id,'')