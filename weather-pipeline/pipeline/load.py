"""Load: flatten raw JSON files into DuckDB raw tables, idempotently.

Idempotency comes from PRIMARY KEY (city, ts) + INSERT OR REPLACE:
re-running a day overwrites the same rows instead of duplicating them.
"""
import datetime as dt
import json
import logging
from pathlib import Path

import duckdb
import pandas as pd

from pipeline.config import DB_PATH, RAW_DIR, SOURCES

log = logging.getLogger(__name__)

DDL = {
    "raw_weather": """
        CREATE TABLE IF NOT EXISTS raw_weather (
            city VARCHAR,
            ts TIMESTAMP,
            temperature_2m DOUBLE,
            relative_humidity_2m DOUBLE,
            precipitation DOUBLE,
            wind_speed_10m DOUBLE,
            loaded_at TIMESTAMP,
            PRIMARY KEY (city, ts)
        )""",
    "raw_air_quality": """
        CREATE TABLE IF NOT EXISTS raw_air_quality (
            city VARCHAR,
            ts TIMESTAMP,
            pm10 DOUBLE,
            pm2_5 DOUBLE,
            us_aqi DOUBLE,
            loaded_at TIMESTAMP,
            PRIMARY KEY (city, ts)
        )""",
}


def connect(db_path: Path = DB_PATH) -> duckdb.DuckDBPyConnection:
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(db_path))
    for ddl in DDL.values():
        con.execute(ddl)
    return con


def flatten(payload: dict, city: str) -> pd.DataFrame:
    """Turn Open-Meteo's column-oriented 'hourly' block into one row per hour."""
    df = pd.DataFrame(payload["hourly"]).rename(columns={"time": "ts"})
    df["ts"] = pd.to_datetime(df["ts"])
    df.insert(0, "city", city)
    df["loaded_at"] = pd.Timestamp.now(tz="UTC").tz_localize(None)
    # JSON nulls become NaN in pandas; convert to real NULLs for the database.
    return df.astype(object).where(df.notna(), None)


def load_file(con: duckdb.DuckDBPyConnection, path: Path, source: str) -> int:
    cfg = SOURCES[source]
    payload = json.loads(Path(path).read_text())
    df = flatten(payload, city=Path(path).stem)
    cols = ["city", "ts", *cfg["variables"], "loaded_at"]
    con.register("incoming", df)
    con.execute(
        f"INSERT OR REPLACE INTO {cfg['table']} ({', '.join(cols)}) "
        f"SELECT {', '.join(cols)} FROM incoming"
    )
    con.unregister("incoming")
    return len(df)


def load_all(run_date: dt.date | None = None, raw_dir: Path = RAW_DIR,
             db_path: Path = DB_PATH) -> int:
    run_date = run_date or dt.date.today()
    con = connect(db_path)
    total = 0
    try:
        for source in SOURCES:
            for path in sorted((raw_dir / run_date.isoformat() / source).glob("*.json")):
                n = load_file(con, path, source)
                log.info("Loaded %s rows from %s", n, path)
                total += n
    finally:
        con.close()
    return total


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    load_all()
