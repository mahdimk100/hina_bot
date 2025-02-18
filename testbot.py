import telebot
import requests
import json
import threading
import time
from flask import Flask, request
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# توکن ربات تلگرام
TOKEN = '7564309344:AAG2ulH3R0Ufa77o_P6FaUaXPBk2B69Wpo4'
bot = telebot.TeleBot(TOKEN)

# 🔹 آدرس وب‌سایت شما در PythonAnywhere
WEBHOOK_URL = f"https://yourusername.pythonanywhere.com/{TOKEN}"

# 🔹 آیدی کانال
CHANNEL_ID = "@hina_gold"

# 🔹 API برای دریافت قیمت طلا
API_URL = "https://www.goldapi.io/api/XAU/USD"
API_KEY = "goldapi-ugwhosm797g0nq-io"

HEADERS = {
    "x-access-token": API_KEY,
    "Content-Type": "application/json"
}

# 🔹 تنظیم Flask
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "ربات فعال است!"

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_update = request.get_json()
    bot.process_new_updates([telebot.types.Update.de_json(json_update)])
    return "!", 200

# 🔹 دریافت قیمت‌ها از API
def fetch_prices():
    try:
        response = requests.get(API_URL, headers=HEADERS)
        if response.status_code != 200:
            return None
        data = response.json()
        return data
    except Exception as e:
        print(f"خطا در دریافت قیمت‌ها: {e}")
        return None

# 🔹 ساخت پیام قیمت‌ها
def create_price_message(data):
    try:
        gold_price = data["price"]
        message = f"🏅 قیمت طلای جهانی: {gold_price} دلار در هر اونس"
        return message
    except KeyError:
        return "خطا در پردازش داده‌ها."

# 🔹 دکمه‌های شیشه‌ای
def get_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("وب‌سایت ما", url="https://hinagold.com"))
    markup.add(InlineKeyboardButton("صفحه اینستاگرام", url="https://instagram.com/hina__gold"))
    markup.add(InlineKeyboardButton("ارتباط با ما", url="https://t.me/mahdi_mk100"))
    return markup

# 🔹 هندلر دستور /start
@bot.message_handler(commands=["start"])
def send_welcome(message):
    welcome_text = "به ربات قیمت لحظه‌ای طلا خوش آمدید!"
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_markup())

# 🔹 هندلر دستور /sendprices
@bot.message_handler(commands=["sendprices"])
def send_prices(message):
    data = fetch_prices()
    if data:
        price_message = create_price_message(data)
        bot.send_message(message.chat.id, price_message, reply_markup=get_markup())
    else:
        bot.send_message(message.chat.id, "خطا در دریافت قیمت‌ها.")

# 🔹 ارسال قیمت‌ها به کانال هر 3 ساعت
def send_prices_to_channel():
    while True:
        data = fetch_prices()
        if data:
            price_message = create_price_message(data)
            bot.send_message(CHANNEL_ID, price_message, reply_markup=get_markup())
        time.sleep(10800)  # 3 ساعت

# 🔹 اجرای تابع ارسال قیمت‌ها در یک ترد جداگانه
channel_thread = threading.Thread(target=send_prices_to_channel)
channel_thread.start()

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    app.run(host="0.0.0.0", port=5000)