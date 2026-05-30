from flask import Flask
import time
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "BTC ENGINE TEST RUNNING"

def test_loop():

    while True:

        print("ENGINE LOOP WORKING")

        time.sleep(10)

thread = threading.Thread(target=test_loop)

thread.daemon = True

thread.start()

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=10000)
