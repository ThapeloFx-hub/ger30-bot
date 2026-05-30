from flask import Flask
import os
import requests
import firebase_admin
from firebase_admin import credentials, firestore
import json
import time
from threading import Thread

# FIREBASE SETUP
firebase_key = os.environ.get("FIREBASE_KEY")

firebase_dict = json.loads(firebase_key)

cred = credentials.Certificate(firebase_dict)

firebase_admin.initialize_app(cred)

db = firestore.client()

# FLASK APP
app = Flask(__name__)

@app.route('/')
def home():
    return "BTC ENGINE AUTO RUNNING"

# ENGINE LOOP
def run_engine():

    while True:

        try:

            print("Fetching BTC market data...")

            url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=4h&limit=2"

            response = requests.get(url, timeout=10)

            print("Binance request successful")

            data = response.json()

            print("JSON converted")

            latest = data[-1]

            open_price = float(latest[1])
            close_price = float(latest[4])

            print("OPEN:", open_price)
            print("CLOSE:", close_price)

            # SIMPLE SIGNAL
            if close_price > open_price:

                signal = "BUY"

            else:

                signal = "SELL"

            print("SIGNAL:", signal)

            print("Sending signal to Firebase...")

            db.collection("btc_signals").document("live").set({

                "pair": "BTCUSD",
                "signal": signal,
                "open": open_price,
                "close": close_price,
                "status": "active",
                "timeframe": "H4"

            })

            print("Signal pushed to Firebase")

        except Exception as e:

            print("ERROR:", e)

        time.sleep(60)

# START ENGINE THREAD
engine_thread = Thread(target=run_engine)
engine_thread.daemon = True
engine_thread.start()

# RUN SERVER
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(host="0.0.0.0", port=port)
