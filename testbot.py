
import telebot
import requests
import json
import threading
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# توکن ربات تلگرام
TOKEN = '7564309344:AAG2ulH3R0Ufa77o_P6FaUaXPBk2B69Wpo4'
# آیدی کانال (مثال: '@your_channel_id')
CHANNEL_ID = '@hina_gold'

# آدرس جدید API رایگان
API_URL = 'https://www.goldapi.io/api/XAU/USD'
API_KEY = 'goldapi-ugwhosm797g0nq-io'  # یک API Key رایگان بگیر از سایت goldapi.io


# تنظیمات هدر برای درخواست API
HEADERS = {
    'x-access-token': API_KEY,
    'Content-Type': 'application/json'
}

bot = telebot.TeleBot(TOKEN)

# تابع دریافت قیمت‌ها از وب‌سرویس
def fetch_prices():
    try:
        response = requests.get(API_URL, headers=HEADERS)

        if response.status_code != 200:
            print(f"خطا در دریافت قیمت‌ها: کد وضعیت {response.status_code}")
            return None
        
        data = response.json()
        print("داده‌های دریافت‌شده:", json.dumps(data, indent=4, ensure_ascii=False))  # نمایش داده‌ها برای بررسی
        return data

    except Exception as e:
        print(f"خطا در دریافت قیمت‌ها: {e}")
        return None

# تابع ساخت پیام قیمت‌ها
def create_price_message(data):
    try:
        gold_price = data['price']
        message = (
            f"🏅 قیمت طلای جهانی: {gold_price} دلار در هر اونس\n"
        )
        return message
    except KeyError as e:
        print(f"کلید مورد نظر یافت نشد: {e}")
        return "خطا در پردازش داده‌ها."

# دکمه‌های شیشه‌ای
def get_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("وب‌سایت ما", url="https://yourwebsite.com"))
    markup.add(InlineKeyboardButton("صفحه اینستاگرام", url="https://instagram.com/yourpage"))
    markup.add(InlineKeyboardButton("ارتباط با ما", url="https://t.me/yourtelegram"))
    return markup

# هندلر دستور /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "به ربات قیمت لحظه‌ای طلا خوش آمدید!\n"
        "با استفاده از این ربات می‌توانید از آخرین قیمت‌های بازار مطلع شوید."
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_markup())

# هندلر دستور /sendprices
@bot.message_handler(commands=['sendprices'])
def send_prices(message):
    data = fetch_prices()
    if data:
        price_message = create_price_message(data)
        bot.send_message(message.chat.id, price_message, reply_markup=get_markup())
    else:
        bot.send_message(message.chat.id, "خطا در دریافت قیمت‌ها. لطفاً بعداً دوباره امتحان کنید.")

# تابع ارسال قیمت‌ها به کانال
def send_prices_to_channel():
    while True:
        current_hour = time.localtime().tm_hour
        if 11 <= current_hour <= 23:
            data = fetch_prices()
            if data:
                price_message = create_price_message(data)
                bot.send_message(CHANNEL_ID, price_message, reply_markup=get_markup())
            else:
                bot.send_message(CHANNEL_ID, "خطا در دریافت قیمت‌ها.")
        time.sleep(10800)  # 3 ساعت

# اجرای تابع ارسال قیمت‌ها به کانال در یک ترد جداگانه
channel_thread = threading.Thread(target=send_prices_to_channel)
channel_thread.start()

bot.infinity_polling(timeout=10, long_polling_timeout=5)

# شروع ربات
bot.polling()
