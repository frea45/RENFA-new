import time
from pyrogram import Client, filters
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)
from helper.database import find_one, used_limit
from helper.database import daily as daily_
import datetime
from datetime import datetime
from datetime import date as date_
from helper.progress import humanbytes
from helper.database import daily as daily_
from helper.date import check_expi
from helper.database import uploadlimit, usertype


@Client.on_message(filters.private & filters.command(["myplan"]))
async def start(client, message):
    used_ = find_one(message.from_user.id)
    daily = used_["daily"]
    expi = daily - \
        int(time.mktime(time.strptime(str(date_.today()), '%Y-%m-%d')))
    if expi != 0:
        today = date_.today()
        pattern = '%Y-%m-%d'
        epcho = int(time.mktime(time.strptime(str(today), pattern)))
        daily_(message.from_user.id, epcho)
        used_limit(message.from_user.id, 0)
    _newus = find_one(message.from_user.id)
    used = _newus["used_limit"]
    limit = _newus["uploadlimit"]
    remain = int(limit) - int(used)
    user = _newus["usertype"]
    ends = _newus["prexdate"]
    if ends:
        pre_check = check_expi(ends)
        if pre_check == False:
            uploadlimit(message.from_user.id, 1288490188) #2147483652
            usertype(message.from_user.id, "Free")
    if ends == None:
        text = f"**🔺 نام کاربر :** {message.from_user.mention}\n**🔺آیدی عددی شما :** `{message.from_user.id}` \n**🔮 پلن فعلی شما :** {user} \n💽 حجم محدودیت روزانه : {humanbytes(limit)} \n✅ حجم استفاده شده : {humanbytes(used)} \n☑️ حجم باقی مانده : {humanbytes(remain)} \n📊 استفاده شده: {percent:.1f}%\n{bar}\n⌚ فاصله زمانی بین فایل ها : 60ثانیه\n**"
    else:
        normal_date = datetime.fromtimestamp(ends).strftime('%Y-%m-%d')
        text = f"**🔺 نام کاربر :** {message.from_user.mention}\n**🔺آیدی عددی شما : `{message.from_user.id}`\n🔮 پلن فعلی شما : {user} \n💽 حجم محدودیت روزانه : {humanbytes(limit)} \n✅ حجم استفاده شده : {humanbytes(used)} \n☑️ حجم باقی مانده : {humanbytes(remain)} \n📊 استفاده شده: {percent:.1f}%\n{bar}\n⌚ فاصله زمانی بین فایل ها : ندارد\n📆 تاریخ اتمام پلن : {normal_date} **"

    if user == "Free":
        await message.reply(text, quote=True, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔖 ارتقا پلن ", callback_data="upgrade"), InlineKeyboardButton("✖️ بستن", callback_data="cancel")]]))
    
    elif usertype == "Gift":
        plan_name = "پلن هدیه ۷ روزه"
        expire = datetime.fromtimestamp(user.get("daily")).strftime("%Y-%m-%d %H:%M")
        bar = progress_bar(used_today, daily_limit)
        percent = round(used_today / daily_limit * 100, 1)
        percent_text = f"{percent}".rstrip("0").rstrip(".") if percent % 1 == 0 else f"{percent}"
        text = f"""🎁 {plan_name}

⏱ تا تاریخ: {expire}
📊 مصرف امروز: {humanbytes(used_today)} / {humanbytes(daily_limit)} ({percent_text}%)
{bar}
"""
        await message.reply_text(text)
        return



    elif usertype == "VIP15":
        plan_name = "VIP پانزده‌روزه"
        expire_ts = user.get("daily")
        expire = datetime.fromtimestamp(expire_ts).strftime("%Y-%m-%d %H:%M")
        remaining_days = max(0, (expire_ts - int(time.time())) // 86400)
        used_str = humanbytes(used_today)
        remain_str = humanbytes(daily_limit - used_today)
        total_limit_str = humanbytes(daily_limit)
        bar = progress_bar(used_today, daily_limit)
        percent = round(used_today / daily_limit * 100, 1)
        percent_text = f"{percent}".rstrip("0").rstrip(".") if percent % 1 == 0 else f"{percent}"
        name = message.from_user.first_name
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

# این بخش دیگه نیازی به else نداره چون return زدی
await message.reply(
    text,
    quote=True,
    reply_markup=InlineKeyboardMarkup(
        [[InlineKeyboardButton("✖️ بستن ✖️", callback_data="cancel")]]
    )
)
      
