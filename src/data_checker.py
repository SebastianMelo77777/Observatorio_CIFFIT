import requests
import json
from pathlib import Path

def has_new_data(config):
    last_file = Path(config["paths"]["last_update_file"])
    if not last_file.exists():
        return True
    with open(last_file) as f:
        last = json.load(f)
    resp = requests.get(config["urls"]["metadata_url"], timeout=30)
    current = resp.json()
    return current.get("rowsUpdatedAt") != last.get("rowsUpdatedAt")