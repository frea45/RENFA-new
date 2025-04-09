
import time
from pyrogram import filters
from pyrogram.types import Message
from config import FREE_PLAN
#from database.access import db
from datetime import datetime
from loader import app

GIFT_DAYS = 7
GIFT_DAILY_LIMIT = 5 * 1024 * 1024 * 1024  # 5GB

@app.on_message(filters.command("gift"))
async def gift_plan_handler(client, message: Message):
    user_id = message.from_user.id
    user = await db.get_user(user_id)

    if user.get("gift_used", False):
        return await message.reply_text("⚠️ شما قبلاً از پلن هدیه یک‌بار استفاده کرده‌اید.")

    now = int(time.time())
    gift_expire = now + GIFT_DAYS * 86400

    await db.update_user(user_id, {
        "daily": gift_expire,
        "limit": GIFT_DAILY_LIMIT,
        "usertype": "Gift",
        "gift_used": True,
        "gift_expired": False
    })

    await message.reply_text(
        f"🎁 پلن هدیه یک هفته‌ای با حجم روزانه 5 گیگابایت برای شما فعال شد!"
        f"تاریخ انقضا: {datetime.fromtimestamp(gift_expire).strftime('%Y-%m-%d %H:%M')}"
    )

# تابع بررسی انقضای پلن هدیه و بازگشت به پلن رایگان + پیام
@app.on_message(filters.all)
async def check_gift_expiry(client, message: Message):
    user_id = message.from_user.id
    user = await db.get_user(user_id)

    if not user:
        return

    usertype = user.get("usertype")
    daily = user.get("daily")
    gift_used = user.get("gift_used", False)
    gift_expired = user.get("gift_expired", False)

    now = int(time.time())
    if usertype == "Gift" and daily and now > daily and gift_used and not gift_expired:
        # بازگشت به پلن رایگان
        await db.update_user(user_id, {
            "usertype": "Free",
            "limit": FREE_PLAN["limit"],
            "daily": 0,
            "gift_expired": True
        })
        try:
            await message.reply_text("⏳ پلن هدیه 7 روزه شما به پایان رسید و پلن رایگان جایگزین شد.")
        except:
            pass
