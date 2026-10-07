"""Extract: call the Open-Meteo APIs and land raw JSON, partitioned by run date.

Layout: data/raw/<YYYY-MM-DD>/<source>/<city>.json
"""
import datetime as dt
import json
import logging
from pathlib import Path

import requests

from pipeline.config import CITIES, RAW_DIR, SOURCES

log = logging.getLogger(__name__)


def fetch(url: str, params: dict) -> dict:
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def extract_city(source: str, city: str, run_date: dt.date, out_dir: Path = RAW_DIR) -> Path:
    lat, lon = CITIES[city]
    cfg = SOURCES[source]
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ",".join(cfg["variables"]),
        "past_days": 1,       # re-fetch yesterday so late corrections are picked up
        "forecast_days": 1,
        "timezone": "UTC",
    }
    payload = fetch(cfg["url"], params)
    target_dir = out_dir / run_date.isoformat() / source
    target_dir.mkdir(parents=True, exist_ok=True)
    path = target_dir / f"{city}.json"
    path.write_text(json.dumps(payload))
    log.info("Wrote %s", path)
    return path


def extract_all(run_date: dt.date | None = None, out_dir: Path = RAW_DIR) -> list[Path]:
    run_date = run_date or dt.date.today()
    paths = []
    for source in SOURCES:
        for city in CITIES:
            paths.append(extract_city(source, city, run_date, out_dir))
    return paths


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    extract_all()
