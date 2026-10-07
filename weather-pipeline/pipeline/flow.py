"""Orchestration with Prefect: extract -> load -> dbt build, with retries and a schedule.

  python -m pipeline.flow            # run once now
  python -m pipeline.flow --serve    # run daily at 06:00 UTC (keeps process alive)
"""
import datetime as dt
import os
import subprocess
import sys

from prefect import flow, task, get_run_logger

from pipeline.config import DBT_DIR, DB_PATH
from pipeline.extract import extract_all
from pipeline.load import load_all


@task(retries=3, retry_delay_seconds=30)
def extract_task(run_date: dt.date):
    return extract_all(run_date)


@task
def load_task(run_date: dt.date):
    return load_all(run_date)


@task
def dbt_task():
    logger = get_run_logger()
    result = subprocess.run(
        ["dbt", "build", "--project-dir", str(DBT_DIR), "--profiles-dir", str(DBT_DIR)],
        capture_output=True, text=True,
        env={**os.environ, "DB_PATH": str(DB_PATH)},
    )
    logger.info(result.stdout)
    if result.returncode != 0:
        raise RuntimeError(f"dbt build failed:\n{result.stdout}\n{result.stderr}")


@flow(name="weather-air-quality-pipeline", log_prints=True)
def pipeline_flow(run_date: dt.date | None = None):
    run_date = run_date or dt.date.today()
    paths = extract_task(run_date)
    rows = load_task(run_date, wait_for=[paths])
    dbt_task(wait_for=[rows])
    print(f"Pipeline finished for {run_date}")


if __name__ == "__main__":
    if "--serve" in sys.argv:
        pipeline_flow.serve(name="daily-weather", cron="0 6 * * *")
    else:
        pipeline_flow()