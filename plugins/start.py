from datetime import date as date_
import datetime
import os
import asyncio
import random
import time
import humanize

from script import *
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant

from helper.progress import humanbytes
from helper.database import (
    botdata, find_one, total_user, insert, used_limit,
    usertype, uploadlimit, addpredata, total_rename, total_size, daily as daily_
)
from helper.date import check_expi
from config import *

bot_username = BOT_USERNAME
log_channel = LOG_CHANNEL
token = BOT_TOKEN
botid = token.split(':')[0]


@Client.on_message(filters.private & filters.command(["start"]))
async def start(client, message):
    user_id = message.chat.id
    insert(int(user_id))

    try:
        id = message.text.split(' ')[1]
    except IndexError:
        id = None

    loading = await message.reply_sticker("CAACAgUAAxkBAAEKVaxlCWGs1Ri6ti45xliLiUeweCnu4AACBAADwSQxMYnlHW4Ls8gQMAQ")
    await asyncio.sleep(1)
    await loading.delete()

    txt = f"""**سلام {message.from_user.mention} 

• به ربات تغییرنام فایل‌ها خوش آمدید 
• هم اکنون یک فایل برایم ارسال کنید تا نام آن را به دلخواه شما تغییر دهم.

سازنده ربات : [FﾑRSみɨの-BﾑŊの](t.me/farshidband)**"""

    await message.reply_photo(
        photo=BOT_PIC,
        caption=txt,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("کانال پشتیبانی", url="https://t.me/ir_botz")],
            [
                InlineKeyboardButton("راهنمای ربات", callback_data='help'),
                InlineKeyboardButton("ارتقا پلن", callback_data='upgrade')
            ]
        ])
    )


@Client.on_message(
    (filters.private & (filters.document | filters.audio | filters.video)) |
    (filters.channel & (filters.document | filters.audio | filters.video))
)
async def send_doc(client, message):
    update_channel = FORCE_SUBS
    user_id = message.from_user.id

    # Force Subscribe
    if update_channel:
        try:
            await client.get_chat_member(update_channel, user_id)
        except UserNotParticipant:
            user_data = find_one(user_id)
            user_plan = user_data.get("usertype", "Free")

            await message.reply_text(
                "<b>• برای استفاده از ربات ابتدا در کانال زیر عضو شوید:\n\nسپس /start بزنید</b>",
                reply_to_message_id=message.id,
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("عضویت", url=f"https://t.me/{update_channel}")
                ]])
            )
            await client.send_message(
                log_channel,
                f"<b>کاربر جدید</b>\n\n"
                f"ID: `{user_id}`\n"
                f"Name: {message.from_user.first_name} {message.from_user.last_name or ''}\n"
                f"Username: @{message.from_user.username or 'ندارد'}\n"
                f"لینک: <a href='tg://openmessage?user_id={}'>کلیک کنید</a>\n"
                f"پلن: {user_plan}".format(user_id),
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("مسدود کردن کاربر", callback_data="ceasepower")
                ]])
            )
            return

    # Bot Stats
    botdata(int(botid))
    bot_info = find_one(int(botid))
    total_renames = bot_info.get('total_rename', 0)
    total_sizes = bot_info.get('total_size', 0)

    user_info = find_one(user_id)
    used_date = user_info.get("date", 0)
    buy_date = user_info.get("prexdate")
    daily_limit = user_info.get("daily", 0)
    user_plan = user_info.get("usertype", "Free")

    # Anti-Spam Timer
    if user_plan == "Free":
        LIMIT = 60
    else:
        LIMIT = 10

    time_left = (used_date + LIMIT) - time.time()
    if time_left > 0:
        await message.reply_text(
            f"**لطفاً {int(time_left)} ثانیه صبر کنید و بعد فایل بفرستید**",
            reply_to_message_id=message.id
        )
        return

    # Get Media
    media = await client.get_messages(message.chat.id, message.id)
    file = getattr(media, "document", None) or getattr(media, "video", None) or getattr(media, "audio", None)
    if not file:
        return

    filename = file.file_name or "Unknown"
    filesize_bytes = file.file_size
    dc_id = FileId.decode(file.file_id).dc_id

    # Daily Limit Check
    today = date_.today()
    expi = daily_limit - int(time.mktime(time.strptime(str(today), '%Y-%m-%d')))
    if expi != 0:
        epcho = int(time.mktime(time.strptime(str(today), '%Y-%m-%d')))
        daily_(user_id, epcho)
        used_limit(user_id, 0)

    current_used = user_info.get("used_limit", 0)
    upload_limit = user_info.get("uploadlimit", 1288490188)  # 1.2 GB default
    remaining = upload_limit - current_used

    if filesize_bytes > remaining:
        await message.reply_text(
            f"سهمیه روزانه شما تمام شده!\n\n"
            f"حجم فایل: {humanbytes(filesize_bytes)}\n"
            f"استفاده شده: {humanbytes(current_used)}\n"
            f"باقی‌مانده: {humanbytes(remaining)}\n\n"
            "برای فایل‌های بزرگ‌تر پلن خود را ارتقا دهید /upgrade",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("ارتقا پلن", callback_data="upgrade")
            ]])
        )
        return

    # 2GB Limit for String Session Bots
    if filesize_bytes > 2147483648:  # 2 GB
        if not STRING:  # If using Bot Token (not userbot)
            await message.reply_text("ربات نمی‌تواند فایل بالای 2GB آپلود کند!")
            return
        else:
            if buy_date and check_expi(buy_date):
                pass  # Premium user with string session → allow
            else:
                await message.reply_text("برای آپلود فایل بالای 2GB باید اکانت پرمیوم داشته باشید.")
                return

    # Free User 500MB Limit
    if user_plan == "Free" and filesize_bytes > 500 * 1024 * 1024:
        await message.reply_text("در پلن رایگان حداکثر 500MB مجاز است.", quote=True)
        return

    # Final Reply
    await message.reply_text(
        f"عالی! حالا برای تغییر نام شروع شود؟\n\n"
        f"نام فعلی: `{filename}`\n"
        f"حجم: {humanbytes(filesize_bytes)}\n"
        f"DC: {dc_id}",
        reply_to_message_id=message.id,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("لغو", callback_data="cancel"),
             InlineKeyboardButton("تغییر نام", callback_data="rename")]
        ])
    )

    # Update Stats
    total_rename(int(botid), total_renames + 1)
    total_size(int(botid), total_sizes, filesize_bytes)
