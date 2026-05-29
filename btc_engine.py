from flask import Flask
import os
import requests

app = Flask(__name__)

@app.route('/')
def home():

    try:

        print("Starting BTC request...")

        url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=4h&limit=1"

        response = requests.get(url, timeout=10)

        print("Request completed")

        data = response.json()

        return {
            "status": "success",
            "data": data
        }

    except Exception as e:

        print("ERROR:", e)

        return {
            "status": "error",
            "message": str(e)
        }

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(host="0.0.0.0", port=port)
