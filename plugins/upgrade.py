from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,ForceReply)
from pyrogram import Client , filters

@Client.on_callback_query(filters.regex('upgrade'))
async def upgrade(bot,update):
	text = """**⭕️ پلن رایگان 🎁 | مشخصات پلن رایگان 🎉
	✓ نامحدود رایگان
	✓ میزان استفاده روزانه : 1 گیگابایت
 ✓ فاصله زمانی بین فایل ها 60ثانیه میباشد.
 💰قیمت : 0 / رایگان 
	
	⭕️ پلن نقره ای 🥈| مشخصات پلن نقره ای🎉 
	✓ یکماهه | 30 روزه
	✓ میزان استفاده روزانه : 10 گیگابایت
 ✓ فاصله زمانی بین فایل ها ندارد
 💰قیمت : 40 هزارتومان
	
	⭕️ پلن طلایی 🥇| مشخصات پلن  طلایی 🎉
	✓ یکماهه | 30 روزه
	✓ میزان استفاده روزانه : 50 گیگابایت
 ✓ فاصله زمانی بین فایل ها ندارد
 💰قیمت : 100 هزارتومان
	
	⭕️ پلن الماسی 💎 | مشخصات پلن الماسی 🎉
	✓ یکماهه | 30 روزه
	✓ میزان استفاده روزانه : 100 گیگابایت
 ✓ فاصله زمانی بین فایل ها ندارد
 💰قیمت : 160 هزارتومان ** """
	keybord = InlineKeyboardMarkup([[ 
        			InlineKeyboardButton("🔖 ارتقای پلن ",url = "https://t.me/ir_botz_support_bot")], 
	                      [  InlineKeyboardButton("🏠 منوی اصلی",callback_data = "home"),
        			 InlineKeyboardButton("✖️ بستن",callback_data = "cancel")]])
	await update.message.edit(text = text,reply_markup = keybord)
	

@Client.on_message(filters.private & filters.command(["upgrade"]))
async def upgradecm(bot,message):
	text = """**⭕️ پلن رایگان 🎁 | مشخصات پلن رایگان 🎉
	✓ نامحدود رایگان
	✓ میزان استفاده روزانه : 1 گیگابایت
 ✓ فاصله زمانی بین فایل ها 60ثانیه میباشد.
 💰قیمت : 0 / رایگان 
	
	⭕️ پلن نقره ای 🥈| مشخصات پلن نقره ای🎉
	✓ یکماهه | 30 روزه
	✓ میزان استفاده روزانه : 10 گیگابایت
 ✓ فاصله زمانی بین فایل ها ندارد
 💰قیمت : 40 هزارتومان
	
	⭕️ پلن طلایی 🥇| مشخصات پلن  طلایی 🎉
        ✓ یکماهه | 30 روزه
	✓ میزان استفاده روزانه : 50 گیگابایت
	✓ فاصله زمانی بین فایل ها ندارد
 💰قیمت : 100 هزارتومان
	
	⭕️ پلن الماسی 💎 | مشخصات پلن الماسی 🎉
	✓ یکماهه | 30 روزه
	✓ میزان استفاده روزانه : 100 گیگابایت
 ✓ فاصله زمانی بین فایل ها ندارد
 💰قیمت : 160 هزارتومان ** """
	keybord = InlineKeyboardMarkup([[ 
        			InlineKeyboardButton("🔖 ارتقای پلن ",url = "https://t.me/ir_botz_support_bot")], 
			      [ InlineKeyboardButton("🏠 منوی اصلی",callback_data = "home"),
        			InlineKeyboardButton("✖️ بستن",callback_data = "cancel")]])
	await message.reply_text(text = text,reply_markup = keybord)








# Jishu Developer 
# Don't Remove Credit 🥺
# Telegram Channel @Madflix_Bots
# Developer @JishuDeveloper
