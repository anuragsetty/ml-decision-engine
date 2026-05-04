PYTHON := .venv/bin/python
PIP := .venv/bin/pip

.PHONY: setup run test lint format check notebook clean

setup:
	python3 -m venv .venv
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) src/main.py

test:
	$(PYTHON) -m pytest -q

lint:
	$(PYTHON) -m ruff check src tests sagemaker

format:
	$(PYTHON) -m black src tests sagemaker

check:
	$(PYTHON) -m black --check src tests sagemaker
	$(PYTHON) -m ruff check src tests sagemaker
	$(PYTHON) -m pytest -q

notebook:
	$(PYTHON) -m jupyter notebook notebooks/01_decision_engine_baseline.ipynb

clean:
	rm -f data/raw/simulated_decision_data.csv data/processed/features.csv models/baseline_logreg.joblib models/metrics.json
