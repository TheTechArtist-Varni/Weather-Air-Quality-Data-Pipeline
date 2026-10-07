import datetime as dt
import json

from pipeline import extract
from pipeline.config import SOURCES
from tests.conftest import sample_payload


def test_extract_city_writes_partitioned_file(tmp_path, monkeypatch):
    monkeypatch.setattr(extract, "fetch", lambda url, params: sample_payload(SOURCES["weather"]["variables"]))
    path = extract.extract_city("weather", "Dubai", dt.date(2026, 10, 1), out_dir=tmp_path)
    assert path == tmp_path / "2026-10-01" / "weather" / "Dubai.json"
    assert "hourly" in json.loads(path.read_text())


def test_extract_sends_expected_params(tmp_path, monkeypatch):
    seen = {}

    def fake_fetch(url, params):
        seen.update(params)
        return sample_payload(SOURCES["air_quality"]["variables"])

    monkeypatch.setattr(extract, "fetch", fake_fetch)
    extract.extract_city("air_quality", "Delft", dt.date(2026, 10, 1), out_dir=tmp_path)
    assert seen["hourly"] == "pm10,pm2_5,us_aqi"
    assert seen["timezone"] == "UTC"
