"""Central configuration: cities, API endpoints, variables, paths."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = Path(os.getenv("RAW_DIR", ROOT / "data" / "raw"))
DB_PATH = Path(os.getenv("DB_PATH", ROOT / "data" / "warehouse.duckdb"))
DBT_DIR = ROOT / "dbt_project"

# name -> (latitude, longitude)
CITIES = {
    "Dubai": (25.20, 55.27),
    "Chennai": (13.08, 80.27),
    "Amsterdam": (52.37, 4.90),
    "Eindhoven": (51.44, 5.48),
    "Delft": (52.01, 4.36),
}

SOURCES = {
    "weather": {
        "url": "https://api.open-meteo.com/v1/forecast",
        "variables": ["temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m"],
        "table": "raw_weather",
    },
    "air_quality": {
        "url": "https://air-quality-api.open-meteo.com/v1/air-quality",
        "variables": ["pm10", "pm2_5", "us_aqi"],
        "table": "raw_air_quality",
    },
}
