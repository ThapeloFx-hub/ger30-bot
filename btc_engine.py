from flask import Flask
from threading import Thread
import time
import os
import requests

# FLASK SERVER
app = Flask(__name__)

@app.route('/')
def home():
    return "BTC ENGINE RUNNING"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# START WEB SERVER
web_thread = Thread(target=run_web)
web_thread.daemon = True
web_thread.start()

print("BTC ENGINE STARTED")

while True:

    try:

        print("Fetching BTC candles...")

        url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=4h&limit=5"

        response = requests.get(url)

        print("Request sent successfully")

        data = response.json()

        print("BTC H4 CANDLES RECEIVED")

        latest_candle = data[-1]

        open_price = latest_candle[1]
        high_price = latest_candle[2]
        low_price = latest_candle[3]
        close_price = latest_candle[4]

        print("LATEST H4 CANDLE:")
        print("OPEN:", open_price)
        print("HIGH:", high_price)
        print("LOW:", low_price)
        print("CLOSE:", close_price)

    except Exception as e:
        print("ERROR:", e)

    time.sleep(60)
