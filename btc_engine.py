from flask import Flask
import os
import requests
import firebase_admin
from firebase_admin import credentials, firestore
import json
import time
import threading

# FIREBASE SETUP

firebase_key = os.environ.get("FIREBASE_KEY")

firebase_dict = json.loads(firebase_key)

cred = credentials.Certificate(firebase_dict)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

# FLASK APP

app = Flask(__name__)

@app.route('/')
def home():
    return "BTC ENGINE AUTO RUNNING"

# SEND SIGNAL FUNCTION

def send_signal(signal_type, price):

    print("Sending Signal to Firebase...")

    signal_data = {

        "pair": "BTCUSDT",
        "signal": signal_type,
        "price": price,
        "status": "active",
        "timeframe": "H4",
        "time": time.strftime("%Y-%m-%d %H:%M:%S")

    }

    db.collection("btc_signals").add(signal_data)

    print("Signal pushed to Firebase!")

# BTC ENGINE LOOP

def btc_engine():

    while True:

        try:

            print("Fetching BTC price from CoinGecko...")

            url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"

            response = requests.get(url, timeout=10)

            print("CoinGecko request successful")

            data = response.json()

            print("JSON converted")

            btc_price = data["bitcoin"]["usd"]

            print(f"BTC Price: {btc_price}")

            # SIMPLE SIGNAL LOGIC

            if btc_price > 80000:

                signal = "SELL"

            else:

                signal = "BUY"

            print(f"Signal Generated: {signal}")

            send_signal(signal, btc_price)

            print("Waiting 60 seconds...\n")

        except Exception as e:

            print("ERROR:", e)

        time.sleep(60)

# START ENGINE THREAD

engine_thread = threading.Thread(target=btc_engine)

engine_thread.daemon = True

engine_thread.start()

print("BTC ENGINE LOOP STARTED")

# RUN FLASK SERVER

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(host="0.0.0.0", port=port)
