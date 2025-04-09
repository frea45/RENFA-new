from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)
from config import *
from pyrogram import Client, filters
from helper.date import add_date
from helper.database import uploadlimit, usertype, addpre


@Client.on_message(filters.private & filters.user(OWNER) & filters.command(["warn"]))
async def warn(c, m):
        if len(m.command) >= 3:
            try:
                user_id = m.text.split(' ', 2)[1]
                reason = m.text.split(' ', 2)[2]
                await m.reply_text("User Notfied Sucessfully 😁")
                await c.send_message(chat_id=int(user_id), text=reason)
            except:
                 await m.reply_text("User Not Notfied Sucessfully 😔")


@Client.on_message(filters.private & filters.user(OWNER) & filters.command(["addpremium"]))

async def buypremium(bot, message):

	await message.reply_text("**🦋 به بخش ارتقا پلن کاربران خوش آمدید.\n\n🚦پلن موردنظر برای کاربر را انتخاب کنید.👇**", quote=True, reply_markup=InlineKeyboardMarkup([		           [

				   InlineKeyboardButton("پلن نقره ای 🥈", callback_data="vip1")

				   ], [

					InlineKeyboardButton("پلن طلایی 🥇", callback_data="vip2")

				   ], [

					InlineKeyboardButton("پلن الماسی 💎", callback_data="vip3")

					]]))

@Client.on_message((filters.channel | filters.private) & filters.user(OWNER) & filters.command(["ceasepower"]))

async def ceasepremium(bot, message):

	await message.reply_text("**♨️میزان کاهش محدودیت روزانه کاربر\nرا انتخاب کنید.**", quote=True, reply_markup=InlineKeyboardMarkup([

		           [InlineKeyboardButton("حجم 500مگابایت", callback_data="cp1"),

				    InlineKeyboardButton("حجم 100مگابایت", callback_data="cp2")

				   ], [

				    InlineKeyboardButton("🧨فعال کردن محدودیت کامل ❌", callback_data="cp3")

				    ]]))


@Client.on_message((filters.channel | filters.private) & filters.user(OWNER) & filters.command(["resetpower"]))

async def resetpower(bot, message):

	    await message.reply_text(text=f"**محدودیت کاربر به روال قبل بازگردد؟\n\n🔺 روزانه 1.2گیگابایت **",quote=True,reply_markup=InlineKeyboardMarkup([

		           [InlineKeyboardButton("✅ بله موافقم 👍",callback_data = "dft")],

				   [InlineKeyboardButton("✖️ کنسل ✖️",callback_data = "cancel")]

				   ]))

@Client.on_callback_query(filters.regex('vip1'))

async def vip1(bot,update):

	id = update.message.reply_to_message.text.split("/addpremium")

	user_id = id[1].replace(" ", "")

	inlimit  = 10737418240

	uploadlimit(int(user_id),10737418240)

	usertype(int(user_id),"**🥈نقره ای**")

	addpre(int(user_id))

	await update.message.edit("**✅ تغییر پلن کاربر باموفقیت انجام شد.\n\n🔮 نوع پلن : نقره ای\n📀 حجم محدودیت روزانه این پلن: 10گیگ**")

	await bot.send_message(user_id,"**✅حساب شما به پلن نقره ای ارتقا پیدا کرد.\n⭕️ هم اکنون بررسی کنید 👈 /myplan **")

	await bot.send_message(log_channel,f"⚡️ Plan Upgraded successfully 💥\n\nHey you are Upgraded To silver. check your plan here /myplan")

@Client.on_callback_query(filters.regex('vip2'))

async def vip2(bot,update):

	id = update.message.reply_to_message.text.split("/addpremium")

	user_id = id[1].replace(" ", "")

	inlimit = 53687091200

	uploadlimit(int(user_id), 53687091200)

	usertype(int(user_id),"**🥇طلایی**")

	addpre(int(user_id))

	await update.message.edit("**✅ تغییر پلن کاربر باموفقیت انجام شد.\n\n🔮 نوع پلن : طلایی\n📀 حجم محدودیت روزانه این پلن: 50گیگ**")

	await bot.send_message(user_id,"**✅ حساب شما به پلن طلایی ارتقا پیدا کرد.\n⭕️ هم اکنون بررسی کنید 👈 /myplan **")

@Client.on_callback_query(filters.regex('vip3'))

async def vip3(bot,update):

	id = update.message.reply_to_message.text.split("/addpremium")

	user_id = id[1].replace(" ", "")

	inlimit = 107374182400

	uploadlimit(int(user_id), 107374182400)

	usertype(int(user_id),"**💎الماسی**")

	addpre(int(user_id))

	await update.message.edit("**✅ تغییر پلن کاربر باموفقیت انجام شد.\n\n🔮 نوع پلن : الماسی\n📀حجم محدودیت روزانه این پلن:100گیگ**")

	await bot.send_message(user_id,"**✅ حساب شما به پلن الماسی ارتقا پیدا کرد.\n⭕️ هم اکنون بررسی کنید 👈 /myplan ")

# CEASE POWER MODE @LAZYDEVELOPER

@Client.on_callback_query(filters.regex('cp1'))

async def cp1(bot,update):

	id = update.message.reply_to_message.text.split("/ceasepower")

	user_id = id[1].replace(" ", "")

	inlimit  = 524288000

	uploadlimit(int(user_id),524288000)

	usertype(int(user_id),"**پلن 500مگابایتی روزانه**")

	addpre(int(user_id))

	await update.message.edit("**⛔️این حساب به سطح پایین افزوده شد.\n\n🔋ظرفیت حجم روزانه کاربر : 500مگابایت**")

	await bot.send_message(user_id,"**❌ هشدار !! \n\n🔋حجم محدودیت روزانه شما به 500MB کاهش یافت.\n\n⭕️ هم اکنون بررسی کنید 👈 /myplan **\n<a href='https://t.me/farshidband'>**📛گزارش-مشکل**</a>")

@Client.on_callback_query(filters.regex('cp2'))

async def cp2(bot,update):

	id = update.message.reply_to_message.text.split("/ceasepower")

	user_id = id[1].replace(" ", "")

	inlimit = 104857600

	uploadlimit(int(user_id), 104857600)

	usertype(int(user_id),"**پلن 100مگابایتی روزانه**")

	addpre(int(user_id))

	await update.message.edit("**⛔️این حساب به سطح پایین افزوده شد.\n\n🔋ظرفیت حجم روزانه کاربر : 100مگابایت**")

	await bot.send_message(user_id,"**❌ هشدار !!\n\n🔋حجم محدودیت روزانه شما به 100MB کاهش یافت.\n\n⭕️ هم اکنون بررسی کنید 👈 /myplan ** \n<a href='https://t.me/farshidband'>**📛گزارش-مشکل**</a>")

@Client.on_callback_query(filters.regex('cp3'))

async def cp3(bot,update):

	id = update.message.reply_to_message.text.split("/ceasepower")

	user_id = id[1].replace(" ", "")

	inlimit = 0

	uploadlimit(int(user_id), 0)

	usertype(int(user_id),"**قطع دسترسی موقت**")

	addpre(int(user_id))

	await update.message.edit("**❌محدودیت کامل برای کاربر افزوده شد.\n\n✔️ محدودیت روزانه = 0 مگابایت**")

	await bot.send_message(user_id,"**⛔️کاربر گرامی دسترسی شما به ربات موقتا\nقطع شد و نمیتوانید فایلی را تغییرنام دهید!**\n\n<a href='https://t.me/farshidband'>**📛 گزارش-مشکل**</a>")


@Client.on_callback_query(filters.regex('dft'))

async def dft(bot,update):

	id = update.message.reply_to_message.text.split("/resetpower")

	user_id = id[1].replace(" ", "")

	inlimit = 1288490188

	uploadlimit(int(user_id), 1288490188)

	usertype(int(user_id),"**رایگان**")

	addpre(int(user_id))

	await update.message.edit("**🔋محدودیت کاربر رفع شد.\n\n♨️ کاربر میتواند روزانه تا 1.2گیگابایت از ربات استفاده کند.و فایل تغییرنام دهد.**")

	await bot.send_message(user_id,"**✅ محدودیت شما برداشته شد.😊\n\n♨️ حساب کاربری تان به روال عادی بازگشت.\n\n⭕️ هم اکنون بررسی کنید 👈 /myplan **")
