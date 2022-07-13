from services.sql import SQLPool
import aiomysql
import asyncio
pool = SQLPool


async def main():
    pool=SQLPool()
    await pool.create()
    cursor:aiomysql.Cursor = await pool.get_cursor()
    await cursor.execute('SELECT * FROM users')
    res=await cursor.fetchall()
    await pool.release_cursor()
    if pool.conn is None:
        print('Yes, the release conn worked')

if __name__ =='__main__':
    asyncio.run(main())