from flask import Flask
import time
import threading
import os
import requests
import firebase_admin
from firebase_admin import credentials, firestore
import json

app = Flask(__name__)

# ====================================
# FIREBASE SETUP
# ====================================

firebase_key = os.environ.get("FIREBASE_KEY")

firebase_dict = json.loads(firebase_key)

cred = credentials.Certificate(firebase_dict)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ====================================
# FLASK ROUTE
# ====================================

@app.route('/')
def home():
    return "BTC ENGINE RUNNING"

# ====================================
# SEND SIGNAL TO FIREBASE
# ====================================

def send_signal(bias, current_price, previous_price):

    print("Sending signal to Firebase...", flush=True)

    signal_data = {

        "pair": "BTCUSD",
        "bias": bias,
        "current_price": current_price,
        "previous_price": previous_price,
        "timeframe": "M5",
        "status": "active",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")

    }

    db.collection("btc_signals").add(signal_data)

    print("Signal pushed to Firebase!", flush=True)

# ====================================
# BTC ENGINE
# ====================================

def btc_loop():

    previous_price = None

    while True:

        try:

            print("=================================", flush=True)
            print("Fetching BTC price...", flush=True)

            url = "https://api.coinbase.com/v2/prices/BTC-USD/spot"

            response = requests.get(url, timeout=10)

            print("Request successful", flush=True)

            data = response.json()

            print("DATA:", data, flush=True)

            # SAFETY CHECK

            if "data" in data:

                btc_price = float(data["data"]["amount"])

                print(f"BTC PRICE: {btc_price}", flush=True)

                # ====================================
                # MARKET STRUCTURE LOGIC
                # ====================================

                if previous_price is not None:

                    print(f"PREVIOUS PRICE: {previous_price}", flush=True)

                    # BUY BIAS

                    if btc_price > previous_price:

                        bias = "BUY"

                    # SELL BIAS

                    elif btc_price < previous_price:

                        bias = "SELL"

                    else:

                        bias = "NEUTRAL"

                    print(f"BIAS: {bias}", flush=True)

                    # SEND TO FIREBASE
                    send_signal(
                        bias,
                        btc_price,
                        previous_price
                    )

                else:

                    print("Collecting first candle data...", flush=True)

                # STORE CURRENT PRICE
                previous_price = btc_price

            else:

                print("Coinbase temporary issue", flush=True)

        except Exception as e:

            print("ERROR:", e, flush=True)

        print("Waiting 5 minutes...\n", flush=True)

        # WAIT 5 MINUTES
        time.sleep(300)

# ====================================
# START ENGINE THREAD
# ====================================

if __name__ == "__main__":

    thread = threading.Thread(target=btc_loop)

    thread.daemon = True

    thread.start()

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
        use_reloader=False
    )
