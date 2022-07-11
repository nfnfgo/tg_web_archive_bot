import time
import asyncio

from telebot.types import User, Message, CallbackQuery, BotCommand


# 用户类
class StatusUser():
    # 关于用户类的全局变量
    users_status_info = {}

    def __init__(self, message: Message = None, id: int | str = None, call: CallbackQuery = None):
        # 依次根据下方顺序尝试获取User的ID（唯一识别标记）
        if id != None:
            id = int(id)
        elif message is not None:
            self.id = int(message.from_user.id)
        elif message is not None:
            self.id = int(call.from_user.id)
        else:
            raise Exception('Failed to initialize a user since no available id data')
        # 尝试读取用户目前状态并写入 user_status （如果用户目前存在状态的话）
        self.status_info = self.get_status(self)

    def __await__(self, message: Message = None, id: int | str = None, call: CallbackQuery = None):
        return self.__init().__await__()

    # 提供await方法（虽然一个异步操作都没有）
    async def __init(self, message: Message = None, id: int | str = None, call: CallbackQuery = None):
        # 依次根据下方顺序尝试获取User的ID（唯一识别标记）
        if id is not None:
            id = int(id)
        elif message is not None:
            self.id = int(message.from_user.id)
        elif message is not None:
            self.id = int(call.from_user.id)
        else:
            raise Exception('Failed to initialize a user since no available id data')

    # 从列表中读取用户的 status_info （如果存在）并写入实例
    def get_status(self):
        '''
        Get Users Status By reading users_status_info

        Return None when user has no status

        Paras:
        self: a StatusUser class instance
        '''
        try:
            self.status_info = self.users_status_info[self.id]
        except Exception:
            self.status_info = None
        finally:
            return self.status_info
    
    def set_status_info(self,**kwargs):
        '''
        Set a user status.

        You can pass a key with empty str or None to delete it, and if it doesn't exist, raise exception
        '''
        timestamp=time.time()
        for item in kwargs.items():
            if (item[1] is None) or (item[1]==''):
                try:
                   del self.status_info[0]
                except Exception as e:
                    print('service/user.py: Failed to del a status_key.',e)
            self.status_info[item[0]]=item[1]
        self.users_status_info[id]=self.set_status_info
    
    def del_status_info(self):
        '''Delete **all** the status of a bot.

        Cautions: This Method doesn't means delete some single keys
        (if you need that please use set_status_info).
        Instead it will delete the whole status_info dictionary 
        of this user, and delete it from users_status_info global list
        '''