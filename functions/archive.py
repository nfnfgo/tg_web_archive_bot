import asyncio
import aiohttp

from telebot.types import Message,CallbackQuery


from config import config
from services import botton
from services.check_url import check_url

# 生成要用的botton
# 在文本检测到网址时进行二次确认
text_active_confirm = botton.gen_markup([['✅继续归档','archive_continue_archive'],['❌取消归档','archive_stop_archive']])

async def archive_url(message,bot,no_comm=True):
    url = message.text
    #判定输入的信息中是指令还是用户直接发送
    for i in ['/archive','/save','/a','/s']:
        if i in url:
            no_comm=False
            print('no commond is False!!!!!')
    print(no_comm)
    if '.' not in url:
        await bot.reply_to(message,'❌*信息读取错误*\n请检查您是否已经在指令后加入正确的网址')
        return

    # if it's by user command, need to clean the command text
    if no_comm is False:
        url=url.split(' ',1)
        try:
            url=url[1]
        except Exception as e:
            print(e)
            await bot.reply_to(message,'❌*信息读取错误*\n请检查您是否已经在指令后加入正确的网址')
            return
    url=check_url(url)
    if no_comm is True:
        await bot.reply_to(message,
        f'⚠️*是否继续归档*\n*网址*{url}\n\nTips: 通过/s指令发出网页归档无需二次确认')
        return
    await bot.reply_to(message,f'📸*正在存档...*\n{url}')

    # start to archive webpage by using aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.get('https://web.archive.org/save/'+url) as res:
            if res.status==200:
                await bot.reply_to(message,f'*✅成功归档*\n[归档页面地址](https://web.archive.org/save/{url})')
            elif res.status==520:
                await bot.reply_to(message,'❌*归档未完成*\nWebArchive服务器出现未知错误，未能完成归档请求')
            elif res.status==404:
                await bot.reply_to(message,'❌*归档未完成*\n网址解析失败，可能为填写的网址不规范或机器人内部发生错误')
            else:
                await bot.reply_to(message,'❌*归档未完成*\n请求出错')

# 接受用户的确认/取消消息并做出响应
async def cbq_confirm_archive(call,bot):
    await botton.del_botton(call,bot)
    if call.data == 'archive_continue_archive':
        await bot.answer_callback_query(call.id,'')
        await bot.reply_to(call.message,f'📸*正在存档...*\n{url}')
        async with session.get('https://web.archive.org/save/'+url) as res:
            message=call.message
            if res.status==200:
                await bot.reply_to(message,f'*✅成功归档*\n[归档页面地址](https://web.archive.org/save/{url})')
            elif res.status==520:
                await bot.reply_to(message,'❌*归档未完成*\nWebArchive服务器出现未知错误，未能完成归档请求')
            elif res.status==404:
                await bot.reply_to(message,'❌*归档未完成*\n网址解析失败，可能为填写的网址不规范或机器人内部发生错误')
            else:
                await bot.reply_to(message,'❌*归档未完成*\n请求出错')
    else:
        await bot.answer_callback_query(call.id,'❎已取消')