import os
import requests
import time

API_KEY = os.getenv("KUCOIN_API_KEY")
API_SECRET = os.getenv("KUCOIN_API_SECRET")
API_PASSPHRASE = os.getenv("KUCOIN_API_PASSPHRASE")
TRADE_AMOUNT = 50  # montant en USDT

def trade():
    print("Démarrage du bot...")
    # Ici tu ajoutes la logique de trading intelligente
    # Ex. : Acheter DOGE si certaines conditions sont réunies
    print(f"Trade simulé de {TRADE_AMOUNT} USDT sur DOGE")

if __name__ == "__main__":
    while True:
        try:
            trade()
            time.sleep(300)  # attend 5 minutes
        except Exception as e:
            print("Erreur:", e)
            time.sleep(60)
