import asyncio
import aiohttp

from telebot.types import Message, CallbackQuery


from config import config
from services import botton
from services.user import UserStatus
from services.check_url import check_url

url_dict = {}

# 生成要用的botton
# 在文本检测到网址时进行二次确认
text_active_confirm = botton.gen_markup([['✅继续归档', 'archive_continue_archive'], ['❌取消归档', 'archive_stop_archive']], row_width=2)


async def archive_url(message, bot):
    url = message.text
    if '.' not in url:
        await bot.reply_to(message, '❌*信息读取错误*\n请检查您是否已经在指令后加入正确的网址')
        return
    # 去除信息中包含的指令，确保此时信息为纯URL
    url = url.split(' ', 1)
    try:
        url = url[1]
    except Exception as e:
        print(e)
        await bot.reply_to(message, '❌*信息读取错误*\n请检查您是否已经在指令后加入正确的网址')
        return
    url = check_url(url)
    archiving_message = await bot.reply_to(message, f'📸<strong>正在存档...</strong> (新页面时间较长，请耐心等待)\n{url}', parse_mode='HTML')

    # start to archive webpage by using aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.get('https://web.archive.org/save/'+url) as res:
            # delete archiving msg
            await bot.delete_message(archiving_message.chat.id, archiving_message.message_id)
            if res.status == 200:
                await bot.send_message(message.from_user.id, f'*✅成功归档*\n[归档页面地址](https://web.archive.org/save/{url})')
            elif res.status == 520:
                await bot.send_message(message.from_user.id, '❌*归档未完成*\nWebArchive服务器出现未知错误，未能完成归档请求')
            elif res.status == 404:
                await bot.send_message(message.from_user.id, '❌*归档未完成*\n网址解析失败，可能为填写的网址不规范或机器人内部发生错误')
            else:
                await bot.send_message(message.from_user.id, '❌*归档未完成*\n请求出错')
                print(res)

# 用户直接发送消息时


async def archive_url_from_text(message, bot):
    print('into the from text function')
    user_status = UserStatus(message=message)
    try:
        # If user has unconfirmed msg, delete it.(Because only new one should be archived)
        old_message = user_status.status_info['archive_confirm_msg'][0]
        await bot.delete_message(old_message.chat.id, old_message.message_id)
        user_status.set_status_info(archive_warn_msg='')
    except:
        pass
    url = message.text
    print('first we got url', url)
    if '.' not in url:
        await bot.reply_to(message, '❌*信息读取错误*\n请检查您是否已经在指令后加入正确的网址')
        return
    url = check_url(url)
    confirm_msg = await bot.reply_to(message, f'⚠️<strong>是否继续归档</strong>\n<strong>网址</strong>:{url}\n\nTips: 通过 /s 指令发出网页归档无需二次确认', reply_markup=text_active_confirm, parse_mode='HTML')
    # Write confrim_msg to status key 'archive_confirm_msg'
    try:
        user_status.set_status_info({'archive_confirm_msg': confirm_msg})
    except Exception as e:
        print('functions/archive.py Failed to write status into a user.', e)
        pass
    try:
        url_dict[message.from_user.id] = url
        print(url_dict)
    except Exception as e:
        print(e)
    return


# 接受用户的确认/取消消息并做出响应
async def cbq_confirm_archive(call, bot):
    print('into the cbq deal function')
    print('okok del')

    if call.data == 'archive_continue_archive':

        # If user confirm archive action, the confirm msg should be deleted
        user_status = UserStatus(call=call)
        archive_confirm_msg = user_status.status_info['archive_confirm_msg'][0]
        await bot.delete_message(archive_confirm_msg.chat.id, archive_confirm_msg.message_id)
        user_status.set_status_info({'archive_confirm_msg': ''})

        print('okok before url')
        try:
            url = url_dict[call.from_user.id]
        except Exception as e:
            print('Failed to read url', e)
        print('after url read')
        await bot.answer_callback_query(call.id, '')
        message = await bot.send_message(call.from_user.id, f'📸<strong>正在存档...</strong> (新页面时间较长，请耐心等待)\n{url}', parse_mode='HTML')
        async with aiohttp.ClientSession() as session:
            async with session.get('https://web.archive.org/save/'+url, timeout=60.0) as res:
                await bot.delete_message(message.chat.id, message.message_id)
                if res.status == 200:
                    await bot.send_message(call.from_user.id, f'*✅成功归档*\n[归档页面地址](https://web.archive.org/save/{url})')
                elif res.status == 520:
                    await bot.send_message(call.from_user.id, '❌*归档未完成*\nWebArchive服务器出现未知错误，未能完成归档请求')
                elif res.status == 404:
                    await bot.send_message(call.from_user.id, '❌*归档未完成*\n网址解析失败，可能为填写的网址不规范或机器人内部发生错误')
                else:
                    await bot.send_message(call.from_user.id, '❌*归档未完成*\n请求出错')
                    print(res)
    else:
        await bot.answer_callback_query(call.id, '❎已取消')
        await botton.del_botton(call, bot)
