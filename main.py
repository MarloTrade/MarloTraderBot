import os
import time
from kucoin.client import Client
from kucoin.exceptions import KucoinAPIException

# Clés API sécurisées via Replit "Secrets"
API_KEY = os.getenv("KUCOIN_API_KEY")
API_SECRET = os.getenv("KUCOIN_API_SECRET")
API_PASSPHRASE = os.getenv("KUCOIN_API_PASSPHRASE")

# Initialisation client KuCoin
client = Client(API_KEY, API_SECRET, API_PASSPHRASE)

# Paramètres du bot
INVEST_AMOUNT = 50  # USDT
TAKE_PROFIT = 1.10  # +10%
STOP_LOSS = 0.97    # -3%

def get_best_pair():
    tickers = client.get_ticker()
    usdt_pairs = [x for x in tickers['ticker'] if x['symbol'].endswith('-USDT') and float(x['changeRate']) > 0]
    sorted_pairs = sorted(usdt_pairs, key=lambda x: float(x['changeRate']), reverse=True)
    return sorted_pairs[0]['symbol'] if sorted_pairs else None

def place_trade(symbol):
    try:
        price = float(client.get_ticker(symbol=symbol)['price'])
        qty = round(INVEST_AMOUNT / price, 4)

        order = client.create_market_order(symbol, 'buy', size=str(qty))
        print(f"Achat exécuté {qty} {symbol} à {price} USDT")

        target_price = price * TAKE_PROFIT
        stop_price = price * STOP_LOSS

        while True:
            time.sleep(10)
            current_price = float(client.get_ticker(symbol=symbol)['price'])

            if current_price >= target_price:
                client.create_market_order(symbol, 'sell', size=str(qty))
                print(f"✅ Take Profit atteint ({current_price:.4f} USDT) – Vente exécutée")
                break
            elif current_price <= stop_price:
                client.create_market_order(symbol, 'sell', size=str(qty))
                print(f"⛔️ Stop Loss atteint ({current_price:.4f} USDT) – Vente exécutée")
                break
            else:
                print(f"[Suivi] {symbol}: {current_price:.4f} USDT")
    except KucoinAPIException as e:
        print(f"Erreur KuCoin: {e}")
    except Exception as ex:
        print(f"Erreur: {ex}")

if __name__ == "__main__":
    pair = get_best_pair()
    if pair:
        print(f"🔍 Meilleure paire trouvée : {pair}")
        place_trade(pair)
    else:
        print("❌ Aucune paire intéressante trouvée.")