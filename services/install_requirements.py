import subprocess
import asyncio


async def install_requirements() -> None:
    '''
    Install the necessary packages through subprocess

    Paras:
    None
    '''
    subprocess.run('pip3 install aiohttp', shell=True)
    subprocess.run('pip3 install aiofiles', shell=True)
    subprocess.run('pip3 install pyTelegramBotAPI', shell=True)

if __name__ == '__main__':
    asyncio.run(install_requirements())
