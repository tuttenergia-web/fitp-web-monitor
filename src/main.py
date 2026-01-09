from scraper import fetch_tournaments
from diff_engine import compare_snapshots, load_snapshot, save_snapshot
from notifier import send_notification
import time

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
                    send_notification(change)

                save_snapshot(new_snapshot)
                old_snapshot = new_snapshot

        except Exception as e:
            print("Errore:", e)

        time.sleep(POLLING_INTERVAL)

if __name__ == "__main__":
    main()