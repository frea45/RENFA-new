from datetime import date as date_
import datetime
import time
import humanize
import asyncio

from script import *
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.file_id import FileId

from helper.progress import humanbytes
from helper.database import (
    botdata, find_one, insert, used_limit, usertype,
    uploadlimit, daily as daily_, total_rename, total_size
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
        _ = message.text.split(' ')[1]
    except IndexError:
        pass

    await asyncio.sleep(0.5)
    txt = f"""سلام {message.from_user.mention}

• به ربات تغییر نام فایل خوش آمدید
• یک فایل بفرستید تا نامش را به دلخواه شما تغییر دهم

سازنده: [FﾑRSみɨの-BﾑŊの](t.me/farshidband)"""

    await message.reply_photo(
        photo=BOT_PIC,
        caption=txt,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("کانال ما", url="https://t.me/ir_botz")],
            [InlineKeyboardButton("راهنما", callback_data='help'),
             InlineKeyboardButton("ارتقا پلن", callback_data='upgrade')]
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
                "<b>برای استفاده از ربات ابتدا در کانال زیر عضو شوید:\n\nبعد از عضویت دوباره /start بزنید</b>",
                reply_to_message_id=message.id,
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("عضویت در کانال", url=f"https://t.me/{update_channel}")
                ]])
            )

            await client.send_message(
                log_channel,
                f"<b>کاربر جدید به ربات پیوست</b>\n\n"
                f"آیدی: `{user_id}`\n"
                f"نام: {message.from_user.first_name} {message.from_user.last_name or ''}\n"
                f"یوزرنیم: @{message.from_user.username or 'ندارد'}\n"
                f"لینک: <a href='tg://user?id={user_id}'>کلیک کنید</a>\n"
                f"پلن: {user_plan}",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("مسدود کردن کاربر", callback_data="ceasepower")
                ]])
            )
            return

    # Bot statistics
    botdata(int(botid))
    bot_info = find_one(int(botid))
    total_renames = bot_info.get('total_rename', 0)
    total_sizes = bot_info.get('total_size', 0)

    user_info = find_one(user_id)
    used_date = user_info.get("date", 0)
    buy_date = user_info.get("prexdate")
    daily_limit = user_info.get("daily", 0)
    user_plan = user_info.get("usertype", "Free")

    # Anti-flood timer
    LIMIT = 60 if user_plan == "Free" else 10
    if time.time() - used_date < LIMIT:
        remaining = int(LIMIT - (time.time() - used_date))
        await message.reply_text(f"لطفاً {remaining} ثانیه صبر کنید و دوباره فایل بفرستید", quote=True)
        return

    # Get file info
    media = await client.get_messages(message.chat.id, message.id)
    file = media.document or media.video or media.audio
    if not file:
        return

    filename = file.file_name or "بدون نام"
    filesize = file.file_size
    dc_id = FileId.decode(file.file_id).dc_id

    # Reset daily limit if new day
    today = date_.today()
    expi = daily_limit - int(time.mktime(time.strptime(str(today), '%Y-%m-%d')))
    if expi != 0:
        daily_(user_id, int(time.mktime(time.strptime(str(today), '%Y-%m-%d'))))
        used_limit(user_id, 0)

    # Daily upload limit check
    used_today = user_info.get("used_limit", 0)
    max_limit = user_info.get("uploadlimit", 1288490188)  # default ~1.2 GB
    if filesize > (max_limit - used_today):
        await message.reply_text(
            f"سهمیه روزانه شما تمام شد!\n\n"
            f"حجم فایل: {humanbytes(filesize)}\n"
            f"استفاده شده امروز: {humanbytes(used_today)}\n"
            f"باقی‌مانده: {humanbytes(max_limit - used_today)}\n\n"
            "برای فایل‌های بزرگ‌تر پلن خود را ارتقا دهید /upgrade",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("ارتقا پلن", callback_data="upgrade")
            ]])
        )
        return

    # 2GB limit for bot token
    if filesize > 2147483648 and not STRING:
        await message.reply_text("ربات با توکن بات نمی‌تواند فایل بالای 2GB آپلود کند!")
        return

    # Free users 500MB limit
    if user_plan == "Free" and filesize > 500 * 1024 * 1024:
        await message.reply_text("در پلن رایگان حداکثر 500MB مجاز است.")
        return

    # Final message
    await message.reply_text(
        f"فایل دریافت شد!\n\n"
        f"نام فعلی: `{filename}`\n"
        f"حجم: {humanbytes(filesize)}\n"
        f"DC: {dc_id}",
        reply_to_message_id=message.id,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("لغو", callback_data="cancel"),
             InlineKeyboardButton("تغییر نام", callback_data="rename")]
        ])
    )

    # Update bot stats
    total_rename(int(botid), total_renames + 1)
    total_size(int(botid), total_sizes, filesize)
