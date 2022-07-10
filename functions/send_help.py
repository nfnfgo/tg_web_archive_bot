import asyncio
import aiohttp

import config.config as config
from services import botton


# set help info
help_text=''
help_text+=f'[{config.bot_disp_name}](https://t.me/{config.bot_username})\n\n' # Bot Title
help_text+='A *bot* help you to archive a webpage simply in Telegram\n'
help_text+=config.sepa+'\n'
help_text+=f'*version:* {config.bot_version}'

# send help function
async def send_help(message,bot):
    get_update_markup=botton.gen_markup([['⏏️检查更新','check_update']])
    await bot.reply_to(message,help_text,reply_markup=get_update_markup)

async def get_update(call,bot):
    await bot.answer_callback_query(call.id,f'✅已经是最新版本: {config.bot_version}')