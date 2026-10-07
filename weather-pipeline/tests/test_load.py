import json

from pipeline import load
from pipeline.config import SOURCES
from tests.conftest import sample_payload


def test_load_is_idempotent(tmp_path):
    src = "weather"
    f = tmp_path / "Dubai.json"
    f.write_text(json.dumps(sample_payload(SOURCES[src]["variables"])))
    con = load.connect(tmp_path / "t.duckdb")

    load.load_file(con, f, src)
    first = con.execute("select count(*) from raw_weather").fetchone()[0]
    load.load_file(con, f, src)  # second run must not duplicate
    second = con.execute("select count(*) from raw_weather").fetchone()[0]

    assert first == second == 24


def test_nulls_become_sql_null(tmp_path):
    f = tmp_path / "Chennai.json"
    f.write_text(json.dumps(sample_payload(SOURCES["weather"]["variables"])))
    con = load.connect(tmp_path / "t.duckdb")
    load.load_file(con, f, "weather")
    nulls = con.execute("select count(*) from raw_weather where temperature_2m is null").fetchone()[0]
    assert nulls == 1
