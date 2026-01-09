import json
import os

SNAPSHOT_FILE = "src/snapshot.json"

def load_snapshot():
    if not os.path.exists(SNAPSHOT_FILE):
        return []
    with open(SNAPSHOT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_snapshot(snapshot):
    with open(SNAPSHOT_FILE, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)

def compare_snapshots(old, new):
    changes = []

    old_set = {json.dumps(t, sort_keys=True) for t in old}
    new_set = {json.dumps(t, sort_keys=True) for t in new}

    added = new_set - old_set
    removed = old_set - new_set

    for a in added:
        torneo = json.loads(a)
        nome = torneo.get("nome_torneo") or torneo.get("nome") or "Sconosciuto"
        changes.append(f"Nuovo torneo rilevato: {nome}")

    for r in removed:
        torneo = json.loads(r)
        nome = torneo.get("nome_torneo") or torneo.get("nome") or "Sconosciuto"
        changes.append(f"Torneo rimosso: {nome}")

    return changes