# About asyncio https://aiomysql.readthedocs.io/en/latest/pool.html

import asyncio
from typing import Coroutine
import aiomysql

import config


# thread poo
class Pool():
    # initialize
    def __init__(self) -> None:
        self.created = False
        print('services/sql.py: Notice, you should use await Pool.create method to create a pool.')
        pass

    # provide await 
    def __await__(self):
        return self.__init().__await__()

    # create thread pool
    async def create(self):
        '''
        Create a pool. And set the created value to True(with no actual check)
        '''
        self.pool = await aiomysql.create_pool(
            host=config.sql_host,
            port=config.sql_port,
            user=config.sql_user,
            password=config.sql_password,
            db=config.sql_db
        )
        self.created=True
