
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)
from pyrogram import Client , filters
from script import *
from config import *



@Client.on_callback_query(filters.regex('about'))
async def about(bot,update):
    text = script.ABOUT_TXT
    keybord = InlineKeyboardMarkup([  
                    [InlineKeyboardButton("🔙 Back",callback_data = "home")]
                  ])
    await update.message.edit(text = text,reply_markup = keybord)


@Client.on_message(filters.private & filters.command(["donate"]))
async def donatecm(bot,message):
	text = script.DONATE_TXT
	keybord = InlineKeyboardMarkup([
        			[InlineKeyboardButton("🦋 Admin",url = "https://t.me/farshidband"), 
        			InlineKeyboardButton("✖️ Close",callback_data = "cancel") ]])
	await message.reply_text(text = text,reply_markup = keybord)

@Client.on_message(filters.private & filters.user(OWNER) & filters.command(["admin"]))
async def admincm(bot,message):
	text = script.ADMIN_TXT
	keybord = InlineKeyboardMarkup([
        			[InlineKeyboardButton("منوی اصلی",callback_data = "home") ]])
	await message.reply_text(text = text,reply_markup = keybord)

@Client.on_callback_query(filters.regex('help'))
async def help(bot,update):
    text = script.HELP_TXT.format(update.from_user.mention)
    keybord = InlineKeyboardMarkup([ 
                    [InlineKeyboardButton('🏞 تنظیم عکس بندانگشتی', callback_data='thumbnail'),
                    InlineKeyboardButton('✏ تنظیم کاپشن', callback_data='caption')],
                    [InlineKeyboardButton('🏠 منوی اصلی', callback_data='home')]
                 #   InlineKeyboardButton('💵 Donate', callback_data='donate')]
                   ])
    await update.message.edit(text = text,reply_markup = keybord)

@Client.on_callback_query(filters.regex('thumbnail'))
async def thumbnail(bot,update):
    text = script.THUMBNAIL_TXT
    keybord = InlineKeyboardMarkup([  
                    [InlineKeyboardButton("بازگشت به منوی قبل",callback_data = "help")]
		  ])
    await update.message.edit(text = text,reply_markup = keybord)

@Client.on_callback_query(filters.regex('caption'))
async def caption(bot,update):
    text = script.CAPTION_TXT
    keybord = InlineKeyboardMarkup([  
                    [InlineKeyboardButton("بازگشت به منوی قبل",callback_data = "help")]
		  ])
    await update.message.edit(text = text,reply_markup = keybord)

@Client.on_callback_query(filters.regex('donate'))
async def donate(bot,update):
    text = script.DONATE_TXT
    keybord = InlineKeyboardMarkup([  
                    [InlineKeyboardButton("بازگشت به منوی قبلی",callback_data = "help")]
		  ])
    await update.message.edit(text = text,reply_markup = keybord)


@Client.on_callback_query(filters.regex('home'))
async def home_callback_handler(bot, query):
    text = f""" **👋 سلام {query.from_user.mention} |🥰😉 \n\n• به ربات تغییرنام فایل ها خوش آمدید ❤️\n\n• هم اکنون یک فایل برایم ارسال کنید تا من\nنام آن را به دلخواه شما تغییر دهم.😊\n\n🖍️ سازنده ربات : [FﾑRSみɨの-BﾑŊの](t.me/farshidband) **"""
    keybord = InlineKeyboardMarkup([  
                    [InlineKeyboardButton("📢 کانال پشتیبانی", url="https://t.me/ir_botz")],
                  #  InlineKeyboardButton("💬 Support", url="https://t.me/HxSupport")],
                   [InlineKeyboardButton("📚 راهنمای ربات", callback_data='help'),
		    InlineKeyboardButton("🏷️ ارتقا پلن", callback_data='upgrade')]
                  #  [InlineKeyboardButton("🧑‍💻 Developer 🧑‍💻", url="https://t.me/Kirodewal")]
		  ])
    await query.message.edit_text(text=text, reply_markup=keybord)
