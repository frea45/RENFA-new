from datetime import timedelta, date, datetime
import time

def add_date(days=30):
    """
    ایجاد تاریخ انقضا بر اساس تعداد روز مشخص.
    خروجی: (تاریخ انقضا به صورت epoch, تاریخ انقضا به صورت YYYY-MM-DD)
    """
    today = date.today()
    ex_date = today + timedelta(days=days)
    pattern = '%Y-%m-%d'
    epcho = int(time.mktime(time.strptime(str(ex_date), pattern)))
    normal_date = datetime.fromtimestamp(epcho).strftime('%Y-%m-%d')
    return epcho, normal_date

def check_expi(saved_date: int) -> bool:
    """
    بررسی می‌کند آیا تاریخ انقضا گذشته یا نه.
    """
    today = date.today()
    pattern = '%Y-%m-%d'
    now_epcho = int(time.mktime(time.strptime(str(today), pattern)))
    return saved_date > now_epcho

def get_remaining_days(saved_date: int) -> int:
    """
    محاسبه تعداد روز باقی‌مانده تا انقضا.
    """
    today = date.today()
    pattern = '%Y-%m-%d'
    now_epcho = int(time.mktime(time.strptime(str(today), pattern)))
    days_left = (saved_date - now_epcho) // 86400  # 86400 ثانیه در روز
    return max(days_left, 0)

def is_two_days_left(saved_date: int) -> bool:
    """
    بررسی می‌کند آیا فقط ۲ روز تا پایان پلن باقی مانده.
    """
    return get_remaining_days(saved_date) == 2
