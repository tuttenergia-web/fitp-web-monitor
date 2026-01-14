import time
import requests
import logging

from scraper import fetch_tournaments
from diff_engine import compare_snapshots, load_snapshot, save_snapshot

# ---------------------------------------------------------
# LOGGING FORENSE
# ---------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info(">>> AVVIO SCRIPT MAIN <<<")

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
        logging.info(f"Telegram status: {r.status_code}")
        return r.status_code == 200
    except Exception as e:
        logging.error(f"Errore Telegram: {e}")
        return False


# ---------------------------------------------------------
# LOOP PRINCIPALE
# ---------------------------------------------------------

POLLING_INTERVAL = 30  # secondi

def main():
    logging.info(">>> LOOP PRINCIPALE AVVIATO <<<")
    print("Avvio monitoraggio pagina FITP...")

    old_snapshot = load_snapshot()
    logging.info(f"Snapshot iniziale caricato: {len(old_snapshot)} tornei")

    while True:
        try:
            logging.info(">>> FETCH TORNEI <<<")
            new_snapshot = fetch_tournaments()
            logging.info(f"Tornei estratti: {len(new_snapshot)}")

            changes = compare_snapshots(old_snapshot, new_snapshot)
            logging.info(f"Variazioni rilevate: {len(changes)}")

            if changes:
                for change in changes:
                    invia_telegram(change)

                save_snapshot(new_snapshot)
                old_snapshot = new_snapshot
                logging.info("Snapshot aggiornato")

        except Exception as e:
            logging.error(f"Errore nel ciclo principale: {e}")

        time.sleep(POLLING_INTERVAL)


if __name__ == "__main__":
    main()