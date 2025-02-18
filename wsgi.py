import sys
import threading
from testbot import bot

# مسیر پروژه رو به sys.path اضافه کن

project_home = r'D:\downloads\hinabot'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# اجرای ربات در یک ترد جداگانه
def run_bot():
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

thread = threading.Thread(target=run_bot)
thread.start()
