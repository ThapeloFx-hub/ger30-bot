from flask import Flask
import time
import threading
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "BTC ENGINE TEST RUNNING"

def test_loop():

    while True:

        print("ENGINE LOOP WORKING", flush=True)

        time.sleep(10)

if __name__ == "__main__":

    thread = threading.Thread(target=test_loop)

    thread.daemon = True

    thread.start()

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
        use_reloader=False
    )
