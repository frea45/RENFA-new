import os, sys, asyncio
from config import *
from pyrogram import filters, Client


@Client.on_message(filters.command("restart") & filters.user(OWNER))
async def stop_button(bot, message):
    msg = await bot.send_message(text="🔄 پروژه ها متوقف شدند در حال ریست...", chat_id=message.chat.id)       
    await asyncio.sleep(3)
    await msg.edit("✅️ ربات با موفقیت ریست شد. 😊")
    os.execl(sys.executable, sys.executable, *sys.argv)



