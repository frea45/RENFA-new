from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from helper.utils import not_subscribed 

@Client.on_message(filters.private & filters.create(not_subscribed))
async def is_not_subscribed(client, message):
    buttons = [[ InlineKeyboardButton(text="✅ عضویت ⚡ ", url=client.invitelink) ]]
    text = "**• برای کارکردن ربات در کانال زیر عضو شوید.\n\n🔚 سپس /start را کلیک کنید.😊👇👇 **"
    await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))
          



