from tradingview_ta import TA_Handler, Interval
import time

print("BTC ENGINE STARTED")

while True:

    try:

        btc = TA_Handler(
            symbol="BTCUSDT",
            screener="crypto",
            exchange="BINANCE",
            interval=Interval.INTERVAL_4_HOURS
        )

        analysis = btc.get_analysis()

        print("BTC H4 SUMMARY:")
        print(analysis.summary)

    except Exception as e:
        print("ERROR:", e)

    time.sleep(60)
