
import asyncio
import time
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database.access import db
from config import BOT_TOKEN
from pyrogram import Client

app = Client("warn_sender", bot_token=BOT_TOKEN)

async def send_plan_warnings():
    users = await db.get_all_users()
    now = int(time.time())

    for user in users:
        ends = user.get("daily")
        warned = user.get("warned", False)

        if ends:
            days_left = (ends - now) // 86400
            if 0 < days_left <= 2 and not warned:
                try:
                    await app.send_message(user["_id"], f"⏳ فقط {days_left} روز تا پایان پلن شما باقی مانده!")
                    await db.update_user(user["_id"], {"warned": True})
                except Exception as e:
                    print(f"خطا در ارسال هشدار به {user['_id']}: {e}")

async def scheduler_main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_plan_warnings, "interval", hours=24, next_run_time=None)
    scheduler.start()

    await app.start()
    await scheduler_main_loop()

async def scheduler_main_loop():
    while True:
        await asyncio.sleep(3600)

asyncio.create_task(scheduler_main())
