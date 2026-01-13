import time
import requests

from scraper import fetch_tournaments
from diff_engine import compare_snapshots, load_snapshot, save_snapshot

# ---------------------------------------------------------
# CONFIGURAZIONE TELEGRAM
# ---------------------------------------------------------

CHAT_ID = "6701954823"
BOT_TOKEN = "8567606681:AAECtRXD-ws0LP8kaIsgAQc9BEAjB2VewHU"

def invia_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": msg,
            "parse_mode": "Markdown"
        }
        r = requests.post(url, json=payload, timeout=20)
        print(f"Telegram status: {r.status_code}")
        return r.status_code == 200
    except Exception as e:
        print(f"Errore Telegram: {e}")
        return False


# ---------------------------------------------------------
# LOOP PRINCIPALE
# ---------------------------------------------------------

POLLING_INTERVAL = 30  # secondi

def main():
    print("Avvio monitoraggio pagina FITP...")

    old_snapshot = load_snapshot()

    while True:
        try:
            new_snapshot = fetch_tournaments()

            changes = compare_snapshots(old_snapshot, new_snapshot)

            if changes:
                for change in changes:
                    invia_telegram(change)

                save_snapshot(new_snapshot)
                old_snapshot = new_snapshot

        except Exception as e:
            print("Errore:", e)

        time.sleep(POLLING_INTERVAL)


if __name__ == "__main__":
    main()