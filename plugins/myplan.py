import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from helper.database import find_one, used_limit, daily as daily_
from helper.database import uploadlimit, usertype
from helper.date import check_expi
from helper.progress import humanbytes
from datetime import datetime, date as date_

@Client.on_message(filters.private & filters.command(["myplan"]))
async def start(client, message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    used_ = find_one(user_id)
    
    # بررسی تاریخ روزانه
    daily = used_["daily"]
    expi = daily - int(time.mktime(time.strptime(str(date_.today()), '%Y-%m-%d')))
    if expi != 0:
        today = date_.today()
        pattern = '%Y-%m-%d'
        epcho = int(time.mktime(time.strptime(str(today), pattern)))
        daily_(user_id, epcho)
        used_limit(user_id, 0)
    
    # دریافت اطلاعات جدید
    _newus = find_one(user_id)
    used = _newus["used_limit"]
    limit = _newus["uploadlimit"]
    remain = int(limit) - int(used)
    user_type = _newus["usertype"]
    ends = _newus["prexdate"]
    
    # بررسی انقضای پلن
    if ends:
        pre_check = check_expi(ends)
        if not pre_check:
            uploadlimit(user_id, 1288490188)  # بازنشانی به پلن رایگان
            usertype(user_id, "Free")

    # محاسبه درصد و نوار پیشرفت
    percent = round((used / limit) * 100, 1) if limit else 0
    percent_text = f"{percent}".rstrip("0").rstrip(".") if percent % 1 == 0 else f"{percent}"
    bar = "▓" * int(percent // 10) + "░" * (10 - int(percent // 10))

    if user_type == "Free":
        text = f"""**🔺 نام کاربر :** {message.from_user.mention}
**🔺 آیدی عددی شما :** `{user_id}`
🔮 **پلن فعلی شما :** {user_type}
💽 **حجم محدودیت روزانه :** {humanbytes(limit)}
✅ **حجم استفاده شده :** {humanbytes(used)}
☑️ **حجم باقی مانده :** {humanbytes(remain)}
📊 **درصد استفاده‌شده:** {percent_text}%
{bar}
⌚ **فاصله بین فایل‌ها:** 60 ثانیه
"""
        await message.reply(text, quote=True, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔖 ارتقا پلن ", callback_data="upgrade"), InlineKeyboardButton("✖️ بستن", callback_data="cancel")]
        ]))
        return

    elif user_type == "Gift":
        plan_name = "پلن هدیه ۷ روزه"
        daily_limit = limit
        used_today = used
        expire = datetime.fromtimestamp(ends).strftime("%Y-%m-%d %H:%M")
        percent = round((used_today / daily_limit) * 100, 1) if daily_limit else 0
        percent_text = f"{percent}".rstrip("0").rstrip(".") if percent % 1 == 0 else f"{percent}"
        bar = "▓" * int(percent // 10) + "░" * (10 - int(percent // 10))
        
        text = f"""🎁 {plan_name}

⏱ **تا تاریخ:** {expire}
📊 **مصرف امروز:** {humanbytes(used_today)} / {humanbytes(daily_limit)} ({percent_text}%)
{bar}
"""
        await message.reply_text(text)
        return

    elif user_type == "VIP15":
        plan_name = "VIP پانزده‌روزه"
        daily_limit = limit
        used_today = used
        expire_ts = ends
        expire = datetime.fromtimestamp(expire_ts).strftime("%Y-%m-%d %H:%M")
        remaining_days = max(0, (expire_ts - int(time.time())) // 86400)
        used_str = humanbytes(used_today)
        remain_str = humanbytes(daily_limit - used_today)
        total_limit_str = humanbytes(daily_limit)
        percent = round((used_today / daily_limit) * 100, 1) if daily_limit else 0
        percent_text = f"{percent}".rstrip("0").rstrip(".") if percent % 1 == 0 else f"{percent}"
        bar = "▓" * int(percent // 10) + "░" * (10 - int(percent // 10))

        text = f"""🔰 وضعیت پلن: {plan_name}

👤 نام کاربر: {name}
🆔 آیدی عددی: `{user_id}`
📦 محدودیت روزانه: {total_limit_str}
📤 حجم مصرف‌شده: {used_str}
📥 حجم باقی‌مانده: {remain_str}
⏳ تاریخ انقضا: {expire}
📆 روزهای باقی‌مانده: {remaining_days}
📊 درصد مصرف‌شده: {percent_text}%
{bar}
"""
        await message.reply_text(text)
        return

    # حالت نهایی (ناشناس یا خطا)
    await message.reply(
        "وضعیت پلن شما قابل شناسایی نیست.",
        quote=True,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("✖️ بستن ✖️", callback_data="cancel")]]
        )
    )
