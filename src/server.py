import threading
import time
from datetime import datetime
from flask import Flask
import main  # contiene fetch_tournaments, detect_new_tournaments, format_torneo, invia_telegram

app = Flask(__name__)

@app.route("/")
def home():
    return "Monitor FITP attivo"

def ts():
    """Restituisce timestamp leggibile."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def monitor_loop():
    print(f"{ts()}  >>> AVVIO THREAD MONITOR FITP <<<")

    while True:
        try:
            print(f"\n{ts()}  [monitor] Avvio ciclo polling…")

            tornei = main.fetch_tournaments()
            totale = len(tornei)
            print(f"{ts()}  [monitor] Trovati {totale} tornei attivi.")

            nuovi = main.detect_new_tournaments(tornei)

            # --- SOLO NUOVI TORNEI ---
            if nuovi:
                print(f"{ts()}  [monitor] Rilevati {len(nuovi)} nuovi tornei:")
                for t in nuovi:
                    msg = main.format_torneo(t)
                    print(f"{ts()}     • {msg}")
                    main.invia_telegram(msg)
            else:
                print(f"{ts()}  [monitor] Nessun nuovo torneo.")

            # --- LOG DEI TORNEI RIMOSSI (solo console, nessuna notifica) ---
            if hasattr(main, "detect_removed_tournaments"):
                rimossi = main.detect_removed_tournaments(tornei)
                if rimossi:
                    print(f"{ts()}  [monitor] Eliminati {len(rimossi)} tornei:")
                    for t in rimossi:
                        print(f"{ts()}     • {main.format_torneo(t)}")
                else:
                    print(f"{ts()}  [monitor] Nessun torneo eliminato.")

        except Exception as e:
            print