# SageMaker Assets

This directory contains **optional** entrypoint scripts you can upload to AWS SageMaker Processing and Training jobs. They reuse logic from `src/decision_engine/` and only depend on packages already listed in the project `requirements.txt`.

## No AWS SDK dependency in this repository

This repo does **not** add `boto3`, `sagemaker`, or other AWS Python SDK packages to `requirements.txt`. Local development and CI stay cloud-agnostic. If you build SageMaker Pipelines or automation in AWS, keep that code in a separate infra repo, a private notebook, or your team’s deployment tooling so this project does not pick up that dependency.

## Files

- `processing.py` — Processing entrypoint for feature generation
- `train.py` — Training entrypoint for model fit + metrics

## Typical SageMaker paths

- Processing input: `/opt/ml/processing/input/`
- Processing output: `/opt/ml/processing/output/`
- Training input: `/opt/ml/input/data/train/`
- Model output: `/opt/ml/model/`

## Next steps

Use `docs/sagemaker_migration.md` for the conceptual mapping to SageMaker (S3, Processing, Training, Registry, etc.). Pipeline definitions and AWS SDK usage belong **outside** this repo if you want to avoid coupling here.
