# About asyncio https://aiomysql.readthedocs.io/en/latest/pool.html

import asyncio
from platform import release

import aiomysql

from config import config


# thread poo
class SQLPool():
    '''
    A Base Pool clase used by this program, instead of the built-in class Pool of aiomysql, 
    this class provide the common function for program
    '''
    # initialize
    pool: aiomysql.Pool = None

    def __init__(self) -> None:
        '''
        Actually don't do anything.

        Use await SQLPool.create to create a available pool.
        '''
        print('services/sql.py: Notice, you should use await Pool.create method to create a pool.')
        self.cursor: aiomysql.Cursor = None
        self.conn: aiomysql.Connection = None

    # provide await
    def __await__(self):
        return self.create().__await__()

    # create thread pool
    async def create(self, force=False) -> aiomysql.Pool:
        '''
        (Asynchronous) Create a pool.

        Remember to use await to call this function

        Paras:
        force: (Bool)(=False) If True, pool will be recreated even if it has a exsiting pool.
        '''
        # create lock, prevent create many times in same time
        pool_creating_lock=asyncio.Lock()
        # if it's a existing pool, and froce=False, than skip creating and retrun existing pool
        if (self.pool is not None) and (force == False):
            return self.pool
        if self.pool is not None:
            await self.delete()
        await pool_creating_lock.acquire()
        try:
            self.pool = await aiomysql.create_pool(
                host=config.sql_host,
                port=config.sql_port,
                user=config.sql_user,
                password=config.sql_password,
                db=config.sql_db
            )
        finally:
            pool_creating_lock.release()

        return self.pool

    # delete pool
    async def delete(self, wait=False) -> None:
        '''
        (Asynchronous) Delete the thread pool

        Paras:
        wait: If true, start a coroutine and waiting for all connection to close actually
        '''
        # set a lock, to prevent del function to be called lots of time in same time
        pool_del_lock = asyncio.Lock()
        # Wait for actual close if wait is True
        if wait:
            async with pool_del_lock:
                await self.pool.wait_closed()
            return
        self.pool.close()

    # distribute a cursor
    async def get_cursor(self) -> aiomysql.Cursor:
        '''
        (Asynchronous) 
        Get a cursor from exsiting pool.

        Will Automatically create a pool or conn if not existing
        '''

        # create a pool if not existing
        if self.pool is None:
            await self.create()

        self.conn = await self.pool.acquire()
        self.cursor = await self.conn.cursor()
        return self.cursor

    async def release_cursor(self) -> None:
        await self.cursor.close()
        self.cursor=None
        self.pool.release(self.conn)
        self.conn=None