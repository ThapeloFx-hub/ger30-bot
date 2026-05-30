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

            print("Fetching BTC price...", flush=True)

            url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"

            response = requests.get(url, timeout=10)

            print("Request successful", flush=True)

            data = response.json()

            print("DATA:", data, flush=True)

            # SAFETY CHECK

            if "bitcoin" in data:

                btc_price = data["bitcoin"]["usd"]

                print(f"BTC PRICE: {btc_price}", flush=True)

            else:

                print("CoinGecko temporary limit reached", flush=True)

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
