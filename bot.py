#!/usr/bin/env python
# coding: utf-8

# In[ ]:

from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
import requests
import time
from datetime import datetime
TOKEN = "8193648355:AAG3IQtsTd2ntcQ_kVYjw9iHoeLxHlwS0Uk"
CHAT_ID = "969493074"
URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd"
prices = {"bitcoin": [], "ethereum": [], "solana": []}  # ذخیره قیمت‌ها
def send_telegram_message(message):
    """ ارسال پیام به تلگرام """
    telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(telegram_url, data=payload)

while True:
    response = requests.get(URL)

    if response.status_code == 200:
        data = response.json()
        btc_price = data["bitcoin"]["usd"]
        eth_price = data["ethereum"]["usd"]
        sol_price = data["solana"]["usd"]

        # ذخیره قیمت‌ها برای تحلیل روزانه
        prices["bitcoin"].append(btc_price)
        prices["ethereum"].append(eth_price)
        prices["solana"].append(sol_price)

        message = f"📊 قیمت ارزها:\n\n" \
                  f"💰 بیت‌کوین: {btc_price} دلار\n" \
                  f"🌐 اتریوم: {eth_price} دلار\n" \
                  f"🚀 سولانا: {sol_price} دلار\n"

        send_telegram_message(message)
        print("✅ پیام ارسال شد!")

    else:
        print("❌ خطا در دریافت اطلاعات")

    # بررسی ارسال گزارش در پایان روز
    now = datetime.now()
    if now.hour == 23 and now.minute == 30:  # ساعت 23:30 گزارش روزانه ارسال کن
        report = "📊 **گزارش روزانه قیمت‌ها:**\n\n"
        for coin in ["bitcoin", "ethereum", "solana"]:
            min_price = min(prices[coin])
            max_price = max(prices[coin])
            avg_price = sum(prices[coin]) / len(prices[coin])
            report += f"💰 **{coin.capitalize()}**\n" \
                      f"🔻 کمترین: {min_price} دلار\n" \
                      f"🔺 بیشترین: {max_price} دلار\n" \
                      f"📉 میانگین: {round(avg_price, 2)} دلار\n\n"
        
        send_telegram_message(report)
        prices = {"bitcoin": [], "ethereum": [], "solana": []}  # ریست کردن داده‌های روزانه
        print("📊 گزارش روزانه ارسال شد!")

    print("⌛ منتظر ۱ ساعت...")
    time.sleep(3600)  # هر ۱ ساعت ارسال کن


# In[ ]:




