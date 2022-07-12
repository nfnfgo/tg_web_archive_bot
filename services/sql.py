# About asyncio https://aiomysql.readthedocs.io/en/latest/pool.html

import asyncio

import aiomysql

from config import config


# thread poo
class SQLPool():
    # initialize
    pool:aiomysql.Pool = None

    def __init__(self) -> None:
        '''
        Actually don't do anything.

        Use await SQLPool.create to create a available pool.
        '''
        print('services/sql.py: Notice, you should use await Pool.create method to create a pool.')
        pass

    # provide await
    def __await__(self):
        return self.create().__await__()

    # create thread pool
    async def create(self, force=False) -> aiomysql.Pool:
        '''
        (Asynchronous) Create a pool. And set the created value to True(with no actual check)

        Remember to use await to call this function

        Paras:
        force: (Bool)(=False) If True, pool will be recreated even if it has a exsiting pool.
        '''
        # if it's a existing pool, and froce=False, than skip creating and retrun existing pool
        if (self.pool is not None) and (force == False):
            return self.pool
        if self.pool is not None:
            self.delete()
        self.pool = await aiomysql.create_pool(
            host=config.sql_host,
            port=config.sql_port,
            user=config.sql_user,
            password=config.sql_password,
            db=config.sql_db
        )
        return self.pool

    # delete pool
    async def delete(self, wait=False) -> None:
        '''
        (Asynchronous) Delete the thread pool

        Paras:
        wait: If true, start a coroutine and waiting for all connection to close actually
        '''
        # Wait for actual close if wait is True
        if wait:
            await self.pool.wait_closed()
            return
        self.pool.close()

    # distribute a cursor
    async def get_cursor(self) -> aiomysql.Cursor:
        '''
        (Asynchronous) 
        Get a cursor from exsiting pool.

        Will Automatically create a pool if not existing
        '''
        return