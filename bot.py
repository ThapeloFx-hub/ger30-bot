import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import requests
import re
import time
import os
import json

# LOAD FIREBASE FROM RENDER ENV VARIABLE
firebase_json = os.environ.get("FIREBASE_KEY")

cred_dict = json.loads(firebase_json)

cred = credentials.Certificate(cred_dict)

firebase_admin.initialize_app(cred)

db = firestore.client()

print("DAX DE40 automation started...")

while True:

    current_time = datetime.now().strftime("%H:%M")

    print(f"Waiting... Current time: {current_time}")

    # ACTIVE TRADING WINDOW
    if "08:55" <= current_time <= "09:10":

        print(f"Reading DAX DE40 data at {current_time}")

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            "https://www.investing.com/indices/germany-40",
            headers=headers
        )

        html = response.text

        # EXTRACT PERCENTAGE INSIDE BRACKETS
        match = re.search(r"\(([+-]?\d+\.\d+)%\)", html)

        if match:

            percentage = match.group(1)

            if float(percentage) > 0:
                direction = "BUY"
                confidence = 90
                status = "Bullish momentum"

            else:
                direction = "SELL"
                confidence = 70
                status = "Bearish momentum"

            # UPDATE FIREBASE
            db.collection("ger30_signals").document("today_signal").set({
                "direction": direction,
                "percentage": percentage,
                "confidence": confidence,
                "status": status,
                "pair": "DAX DE40",
                "time": current_time
            })

            print(f"Firebase updated with {percentage}%")

        else:
            print("Percentage data not found.")

        # WAIT 5 MINUTES
        time.sleep(300)

    else:

        # WAIT 1 MINUTE
        time.sleep(60)
