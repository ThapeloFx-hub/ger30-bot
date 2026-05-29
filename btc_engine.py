from tradingview_ta import TA_Handler, Interval
from flask import Flask
from threading import Thread
import time
import os

# FLASK SERVER
app = Flask(__name__)

@app.route('/')
def home():
    return "BTC ENGINE RUNNING"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# START WEB SERVER
Thread(target=run_web).start()

print("BTC ENGINE STARTED")

while True:

    try:

        print("Fetching BTC data...")

        btc = TA_Handler(
            symbol="BTCUSDT",
            screener="crypto",
            exchange="BINANCE",
            interval=Interval.INTERVAL_4_HOURS
        )

        print("Connecting to TradingView...")

        analysis = btc.get_analysis()

        print("Analysis fetched successfully")

        print("BTC H4 SUMMARY:")
        print(analysis.summary)

    except Exception as e:
        print("ERROR:", e)

    time.sleep(60)
