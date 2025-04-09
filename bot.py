from pyrogram import Client, idle
from plugins.cb_data import app as Client2
from config import *
import asyncio

bot = Client(
    "Renamer",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
    plugins=dict(root='plugins')
)

async def main():
    if STRING:
        apps = [Client2, bot]
        for app in apps:
            await app.start()
        print("All Clients Started")
        await idle()
        for app in apps:
            await app.stop()
        print("All Clients Stopped")
    else:
        await bot.start()
        print("Bot Started (No STRING)")
        await idle()
        await bot.stop()
        print("Bot Stopped")

if __name__ == "__main__":
    asyncio.run(main())
