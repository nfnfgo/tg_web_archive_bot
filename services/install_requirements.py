import subprocess
import asyncio

# Set a install_req_lock
install_req_lock=asyncio.Lock()

async def install_requirements() -> None:
    '''
    Install the necessary packages through subprocess

    Paras:
    None
    '''
    await install_req_lock.acquire()
    try:
        subprocess.run('pip3 install aiohttp', shell=True)
        subprocess.run('pip3 install aiofiles', shell=True)
        subprocess.run('pip3 install pyTelegramBotAPI', shell=True)
    except Error as e:
        print(e)
    finally:
        install_req_lock.release()

if __name__ == '__main__':
    asyncio.run(install_requirements())
