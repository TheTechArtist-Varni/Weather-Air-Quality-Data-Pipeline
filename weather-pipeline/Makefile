.PHONY: setup run test dashboard serve

setup:
	python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

run:
	python -m pipeline.flow

serve:
	python -m pipeline.flow --serve

test:
	pytest -q

dashboard:
	streamlit run dashboard/app.py
