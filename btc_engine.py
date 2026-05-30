from flask import Flask
import time
import threading
import os
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "BTC ENGINE RUNNING"

def btc_loop():

    while True:

        try:

            print("Fetching BTC candle...", flush=True)

            url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=15m&limit=1"

            response = requests.get(url, timeout=10)

            print("Request successful", flush=True)

            data = response.json()

            latest = data[0]

            open_price = latest[1]
            high_price = latest[2]
            low_price = latest[3]
            close_price = latest[4]

            print(f"OPEN: {open_price}", flush=True)
            print(f"HIGH: {high_price}", flush=True)
            print(f"LOW: {low_price}", flush=True)
            print(f"CLOSE: {close_price}", flush=True)

        except Exception as e:

            print("ERROR:", e, flush=True)

        # WAIT 5 MINUTES
        time.sleep(300)

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
