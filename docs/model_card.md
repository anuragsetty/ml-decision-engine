# Model Card: Decision Engine Baseline

## Model Details

- **Model type:** Logistic Regression with `StandardScaler` in a `sklearn.pipeline.Pipeline`
- **Version:** `v0.1-baseline`
- **Owner:** Project maintainer
- **Code location:** `src/decision_engine/models/baseline.py`

## Intended Use

- **Primary use case:** Demonstrate a clean, production-style ML decision pipeline.
- **Users:** Hiring managers, collaborators, and technical reviewers.
- **Out of scope:** Real-world credit, fraud, or healthcare decisions without additional governance.

## Data

- **Source:** Simulated user/transaction/behavior data generated at runtime.
- **Generation module:** `src/decision_engine/data/simulator.py`
- **Target label:** `is_approved`

## Features

- Base behavioral and transactional features plus engineered rates and risk index.
- Feature logic in `src/decision_engine/features/transform.py`.

## Evaluation

- **Split:** Stratified train/test split.
- **Metrics:** Accuracy, ROC AUC, classification report.
- **Output artifact:** `models/metrics.json`

## Risks and Limitations

- Synthetic data may not represent real-world drift or bias patterns.
- Baseline model is linear and intentionally simple.
- No fairness constraints or calibration currently applied.

## Monitoring and Next Steps

- Add drift checks and periodic retraining criteria.
- Compare with tree-based baselines.
- Add threshold tuning and calibration strategy.
