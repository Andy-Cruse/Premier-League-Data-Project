import json
import os
import sys
import time
from dotenv import load_dotenv
from datetime import datetime, timezone
from pathlib import Path

import requests

load_dotenv()

API_KEY = os.environ["FOOTBALL_DATA_API_KEY"]
BASE_URL = "https://api.football-data.org/v4"
RAW_DIR = Path("data/raw")

ENDPOINTS = {
    "matches": "/competitions/PL/matches",
    "standings": "/competitions/PL/standings",
    "teams": "/competitions/PL/teams",
}


def fetch(path, params=None):
    for attempt in range(5):
        resp = requests.get(
            BASE_URL + path,
            headers={"X-Auth-Token": API_KEY},
            params=params,
            timeout=30,
        )
        if resp.status_code == 200:
            return resp.json()
        if resp.status_code == 429 or resp.status_code >= 500:
            time.sleep(5 * 2 ** attempt)
            continue
        resp.raise_for_status()
    raise RuntimeError(f"failed to fetch {path}")


def save(name, season, data):
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    folder = RAW_DIR / name / season
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{ts}.json"
    with open(path, "w") as f:
        json.dump(data, f)
    print("saved", path)


if __name__ == "__main__":
    season = sys.argv[1] if len(sys.argv) > 1 else None
    params = {"season": season} if season else None

    for name, path in ENDPOINTS.items():
        data = fetch(path, params)
        save(name, season or "current", data)
        time.sleep(7)