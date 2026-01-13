import time
import requests
import logging
from bs4 import BeautifulSoup

from diff_engine import compare_snapshots, load_snapshot, save_snapshot

# ---------------------------------------------------------
# CONFIGURAZIONE LOGGING
# ---------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

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
# SCRAPER SENZA PLAYWRIGHT (COMPATIBILE CON RENDER)
# ---------------------------------------------------------

def fetch_tournaments():
    """
    Scarica la pagina FITP e restituisce una lista di tornei.
    Adatta i selettori in base alla struttura reale della tabella FITP.
    """

    url = "https://www.fitp.it/tornei/calendario.html"  # aggiorna se necessario

    logging.info("[monitor] Fetch pagina FITP...")

    response = requests.get(url, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    tornei = []

    # Selettore generico per righe tabella
    rows = soup.select("table tbody tr")

    for row in rows:
        cols = [c.get_text(strip=True) for c in row.find_all("td")]

        # Evita righe vuote o incomplete
        if len(cols) < 5:
            continue

        torneo = {
            "codice": cols[0],
            "nome": cols[1],
            "localita": cols[2],
            "provincia": cols[3],
            "date": cols[4],
        }

        tornei.append(torneo)

    logging.info(f"[monitor] Trovati {len(tornei)} tornei attivi.")
    return tornei


# ---------------------------------------------------------
# LOOP PRINCIPALE
# ---------------------------------------------------------

POLLING_INTERVAL = 30  # secondi

def main():
    logging.info(">>> AVVIO MONITOR FITP (seconda app) <<<")

    old_snapshot = load_snapshot()

    while True:
        try:
            logging.info("[monitor] Avvio ciclo polling...")
            new_snapshot = fetch_tournaments()

            changes = compare_snapshots(old_snapshot, new_snapshot)

            if changes:
                logging.info(f"[monitor] Rilevate {len(changes)} modifiche.")
                for change in changes:
                    invia_telegram(change)

                save_snapshot(new_snapshot)
                old_snapshot = new_snapshot
            else:
                logging.info("[monitor] Nessuna modifica.")

        except Exception as e:
            logging.error(f"Errore nel ciclo principale: {e}")

        time.sleep(POLLING_INTERVAL)


if __name__ == "__main__":
    main()