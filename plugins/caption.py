from pyrogram import Client, filters 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from helper.database import *

@Client.on_message(filters.private & filters.command('set_caption'))
async def add_caption(client, message):
    if len(message.command) == 1:
       return await message.reply_text("**نحوه تنظیم کپشن برای فایل :\n\nابتدا دستور /set_caption نوشته سپس متن موردنظر خود را وارد کنید. نمونه 👇\n👉`/set_caption Hii`**")
    caption = message.text.split(" ", 1)[1]
    addcaption(int(message.chat.id), caption)
    await message.reply_text("**✅ کپشن باموفقیت ذخیره شد.**")

@Client.on_message(filters.private & filters.command('del_caption'))
async def delete_caption(client, message): 
    caption = find(int(message.chat.id))[1]
    if not caption:
        await message.reply_text("**❌ هنوز کپشنی را تنظیم نکرده اید!**")
        return
    delcaption(int(message.chat.id))
    await message.reply_text("**✅ کپشن باموفقیت حذف شد.**")
                                       
@Client.on_message(filters.private & filters.command('see_caption'))
async def see_caption(client, message): 
    caption = find(int(message.chat.id))[1]
    if caption:
       await message.reply_text(f"<b><u>🖍متن کپشن ذخیره شده شما 👇</b></u>\n\n`{caption}`")
    else:
       await message.reply_text("**❌ هنوز کپشنی را تنظیم نکرده اید!**")
          
