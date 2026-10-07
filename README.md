# Weather-Air-Quality-Data-Pipeline


Open-Meteo API -> raw JSON -> DuckDB raw tables -> dbt staging + marts -> Streamlit dashboard, orchestrated by Prefect.

## Quick start
```bash
make setup && source .venv/bin/activate
make run         # extract -> load -> dbt build
make dashboard   # http://localhost:8501
make test        # pytest
make serve       # schedule daily at 06:00 UTC
```

Layout: `pipeline/` (extract, load, flow, config), `dbt_project/` (models + tests), `dashboard/`, `tests/`.
See the accompanying guide for a step-by-step explanation.
