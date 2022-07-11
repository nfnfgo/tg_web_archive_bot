import time
import asyncio

from telebot.types import User, Message, CallbackQuery, BotCommand


# 用户类
class StatusUser():
    def __init__(self, message: Message = None, id: int | str = None, call: CallbackQuery = None):
        # 依次根据下方顺序尝试获取User的ID（唯一识别标记）
        if id != None:
            id=int(id)
        elif message != None:
            self.id = int(message.from_user.id)
        elif message != None:
            self.id=int(call.from_user.id)
        else:
            raise Exception('Failed to initialize a user since no available id data')
    
    def __await__(self, message: Message = None, id: int | str = None, call: CallbackQuery = None):
        return self.__init.__await__()

    # 提供await方法（虽然一个异步操作都没有）
    async def __init(self, message: Message = None, id: int | str = None, call: CallbackQuery = None):
        # 依次根据下方顺序尝试获取User的ID（唯一识别标记）
        if id != None:
            id=int(id)
        elif message != None:
            self.id = int(message.from_user.id)
        elif message != None:
            self.id=int(call.from_user.id)
        else:
            raise Exception('Failed to initialize a user since no available id data')
        return