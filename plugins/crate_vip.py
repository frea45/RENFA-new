
from pyrogram import filters
from pyrogram.types import Message
from bot import bot as app

from database.access import db
from datetime import datetime, timedelta
import time
import random
import string

VIP_DAYS = 15
VIP_DAILY_LIMIT = 5 * 1024 * 1024 * 1024  # 5 گیگ

vip_codes = {}

def generate_code(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# فقط ادمین‌ها می‌توانند کد VIP بسازند
ADMINS = [ADMIN_ID_1, ADMIN_ID_2]  # شناسه عددی ادمین‌ها را اینجا وارد کنید

@app.on_message(filters.command("crate_vip"))
async def create_vip(client, message: Message):
    if message.from_user.id not in ADMINS:
        return await message.reply_text("⛔️ فقط ادمین می‌تواند کد VIP بسازد.")
    
    code = generate_code()
    vip_codes[code] = {"used": False}
    await message.reply_text(f"✅ کد VIP یکبار مصرف ساخته شد:\n`/vip {code}`")

@app.on_message(filters.command("vip"))
async def redeem_vip(client, message: Message):
    user_id = message.from_user.id
    user = await db.get_user(user_id)

    if len(message.command) < 2:
        return await message.reply_text("❗️ لطفاً کد VIP را وارد کنید.\nمثال: `/vip abc123xyz`", quote=True)

    code = message.command[1]

    if code not in vip_codes:
        return await message.reply_text("❌ کد VIP نامعتبر است.")
    
    if vip_codes[code]["used"]:
        return await message.reply_text("⚠️ این کد قبلاً استفاده شده است.")

    # بررسی اینکه فقط کاربران رایگان بتوانند استفاده کنند
    if user.get("usertype") != "Free":
        return await message.reply_text("⛔️ فقط کاربران پلن رایگان می‌توانند از کد VIP استفاده کنند.")

    now = int(time.time())
    expire = now + VIP_DAYS * 86400

    await db.update_user(user_id, {
        "daily": expire,
        "limit": VIP_DAILY_LIMIT,
        "usertype": "VIP15",
        "vip_used": True
    })

    vip_codes[code]["used"] = True

    await message.reply_text(
        f"🎉 پلن VIP پانزده‌روزه با حجم روزانه ۵ گیگابایت برای شما فعال شد."
        f"تاریخ انقضا: {datetime.fromtimestamp(expire).strftime('%Y-%m-%d %H:%M')}"
    )
