import kucoin.client
import os

API_KEY = os.getenv("KUCOIN_API_KEY")
API_SECRET = os.getenv("KUCOIN_API_SECRET")
PASSPHRASE = os.getenv("KUCOIN_API_PASSPHRASE")

client = kucoin.client.Client(API_KEY, API_SECRET, PASSPHRASE)

def buy(pair, amount):
    try:
        order = client.create_market_order(pair, side='buy', funds=amount)
        print("Trade OK :", order)
    except Exception as e:
        print("Erreur :", e)

if __name__ == "__main__":
    buy("DOGE-USDT", "50")
