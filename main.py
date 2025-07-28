import os
from kucoin.client import Client
from kucoin.exceptions import KucoinAPIException
import time

# Charger les clés API depuis les variables d'environnement
api_key = os.getenv("KUCOIN_API_KEY")
api_secret = os.getenv("KUCOIN_API_SECRET")
api_passphrase = os.getenv("KUCOIN_API_PASSPHRASE")

client = Client(api_key, api_secret, api_passphrase)

def get_best_pair():
    tickers = client.get_ticker()
    best_pair = None
    max_change = -9999

    for ticker in tickers['ticker']:
        symbol = ticker['symbol']
        if symbol.endswith("-USDT"):
            try:
                change_rate = float(ticker['changeRate'])
                if change_rate > max_change:
                    max_change = change_rate
                    best_pair = symbol
            except:
                continue

    return best_pair

def place_order(symbol, usdt_amount):
    try:
        # Récupérer les infos de la paire
        symbol_info = client.get_symbol(symbol)
        min_size = float(symbol_info['baseMinSize'])
        increment = float(symbol_info['baseIncrement'])

        # Obtenir le prix actuel
        price_info = client.get_ticker(symbol=symbol)
        price = float(price_info['price'])

        # Calculer la quantité à acheter
        raw_qty = usdt_amount / price
        adjusted_qty = round(raw_qty / increment) * increment

        if adjusted_qty < min_size:
            print(f"❌ Quantité trop faible pour {symbol}. Minimum requis : {min_size}")
            return

        print(f"🔁 Quantité ajustée pour {symbol} : {adjusted_qty}")

        # Placer l'ordre
        order = client.create_market_order(symbol=symbol, side='buy', size=str(adjusted_qty))
        print(f"✅ Ordre passé pour {symbol} : {order}")

    except KucoinAPIException as e:
        print(f"❌ Erreur KuCoin : {e}")
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")

def main():
    print("🔁 Démarrage du bot MarloTraderBot...")
    best_pair = get_best_pair()
    if best_pair:
        print(f"🔍 Meilleure paire trouvée : {best_pair}")
        place_order(best_pair, usdt_amount=10)
    else:
        print("❌ Aucune paire USDT trouvée.")

if __name__ == "__main__":
    while True:
        main()
        time.sleep(300)