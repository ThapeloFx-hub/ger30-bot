import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import requests
import re
import time

# FIREBASE SETUP
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

print("DAX DE40 automation started...")

while True:

    current_time = datetime.now().strftime("%H:%M")

    print(f"Waiting... Current time: {current_time}")

    # ACTIVE TRADING WINDOW
    if "08:55" <= current_time <= "09:10":

        print(f"Reading DAX DE40 data at {current_time}")

        # INVESTING.COM REQUEST
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

            # SIGNAL LOGIC
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

        # WAIT 5 MINUTES DURING ACTIVE WINDOW
        time.sleep(300)

    else:

        # WAIT 1 MINUTE OUTSIDE ACTIVE WINDOW
        time.sleep(60)