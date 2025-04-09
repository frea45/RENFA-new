from config import *
from pyrogram import Client, filters
from pyrogram.types import ( InlineKeyboardButton, InlineKeyboardMarkup)
from helper.database import botdata, find_one, total_user,getid
from helper.progress import humanbytes

token = BOT_TOKEN
botid = token.split(':')[0]

@Client.on_message(filters.private & filters.user(OWNER)  & filters.command(["users"]))
async def users(client,message):
	botdata(int(botid))
	data = find_one(int(botid))
	total_rename = data["total_rename"]
	total_size = data["total_size"]
	id = str(getid())
	ids = id.split(',')

	await message.reply_text(f"**👥 تعداد کاربران ربات :- {total_user()} کاربر\n\n📂 تعداد فایل های تغییرنام داده شده:\n• :- {total_rename}\n🔋سایز فایل های تغییرنام داده شده:\n :- {humanbytes(int(total_size))} **",quote=True,
                             reply_markup= InlineKeyboardMarkup([[InlineKeyboardButton("بستن", callback_data="cancel")]]) 
                             )
	
@Client.on_message(filters.private & filters.user(OWNER)  & filters.command(["allids"]))
async def allids(client,message):
	botdata(int(botid))
	data = find_one(int(botid))
	total_rename = data["total_rename"]
	total_size = data["total_size"]
	id = str(getid())
	ids = id.split(',')

	await message.reply_text(f"⚡️ **All IDs** :- {ids}\n\n⚡️ **Total User** :- {total_user()}\n\n⚡️ **Total Renamed File** :- {total_rename}\n⚡ **Total Size Renamed** :- {humanbytes(int(total_size))}",quote=True,
                             reply_markup= InlineKeyboardMarkup([[InlineKeyboardButton("بستن", callback_data="cancel")]]) 
                             )	


