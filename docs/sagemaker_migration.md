# SageMaker Migration Guide

This guide describes how to migrate this local ML decision engine into a production-oriented AWS SageMaker workflow.

**Dependency policy:** This repository keeps `requirements.txt` free of AWS SDKs (`boto3`, `sagemaker`, etc.). Use the scripts under `sagemaker/` as job entrypoints only; define pipelines, IAM, and infrastructure in AWS or in a separate repository if you do not want this codebase to depend on the SageMaker Python SDK.

## 1) Target Architecture

Use a managed pipeline with these core stages:

1. **Data input** from Amazon S3
2. **Feature processing** using SageMaker Processing jobs
3. **Model training** using SageMaker Training jobs
4. **Model registration** in SageMaker Model Registry
5. **Approval + deployment** to Endpoint or Batch Transform
6. **Monitoring + retraining triggers** with Model Monitor + EventBridge

## 2) Map Local Modules to SageMaker Steps

- `src/decision_engine/data/simulator.py`
  - Local prototype for synthetic input generation
  - In cloud: replace with upstream S3 data ingestion or scheduled synthetic generation job
- `src/decision_engine/features/transform.py`
  - Convert into a SageMaker Processing script (`processing.py`)
- `src/decision_engine/models/baseline.py`
  - Convert into a SageMaker training entrypoint (`train.py`)
- `src/decision_engine/pipeline.py`
  - Logical blueprint for SageMaker Pipelines step graph
- `docs/model_card.md`
  - Attach to model review and approval process

## 3) Migration Phases

## Phase 1: Packaging and Entrypoints

This repo includes reference entrypoints:

- `sagemaker/processing.py` — reads raw CSV from `/opt/ml/processing/input`, applies feature transforms, writes features to `/opt/ml/processing/output`
- `sagemaker/train.py` — reads features from `/opt/ml/input/data/train`, trains the baseline model, writes `model.joblib` under `/opt/ml/model` and metrics JSON under `/opt/ml/output`

Deliverable: scripts runnable in SageMaker containers (and testable locally with the same paths if you mount data).

## Phase 2: Pipeline Definition

Define SageMaker Pipelines (ProcessingStep, TrainingStep, RegisterModel, etc.) **outside this repository**—for example in an infra repo, deployment package, or internal tooling—so this project does not take a dependency on the SageMaker Python SDK. Alternatively use the SageMaker Studio UI and job definitions while still reusing `sagemaker/processing.py` and `sagemaker/train.py` as uploaded scripts.

Deliverable: reproducible, versioned pipeline execution in your AWS environment.

## Phase 3: Deployment and Inference

- For realtime:
  - Deploy approved model package to SageMaker Endpoint
- For async/batch:
  - Use Batch Transform jobs from approved model package

Deliverable: stable inference path with clear promotion process.

## Phase 4: Monitoring and Retraining

- Enable Model Monitor (data quality + model quality where labels are available)
- Publish metrics to CloudWatch
- Trigger retraining pipeline through EventBridge rules

Deliverable: closed-loop ML lifecycle with drift-aware retraining.

## 4) Recommended AWS Services

- **Storage:** Amazon S3
- **Feature management:** SageMaker Feature Store (optional)
- **Pipeline orchestration:** SageMaker Pipelines
- **Experiment tracking:** SageMaker Experiments
- **Model governance:** SageMaker Model Registry
- **Serving:** SageMaker Endpoints or Batch Transform
- **Monitoring:** Model Monitor + CloudWatch
- **Automation:** EventBridge + Lambda/Step Functions (optional)

## 5) IAM and Security Basics

- Use least-privilege IAM roles for:
  - Processing jobs
  - Training jobs
  - Pipeline execution
  - Endpoint hosting
- Encrypt S3 buckets and artifacts (SSE-S3 or SSE-KMS)
- Enable VPC networking for jobs/endpoints if required by policy
- Track approvals and lineage through Model Registry

## 6) CI/CD Integration Pattern

Use CI to automate quality checks and controlled deployment:

1. Run lint/test on pull request
2. Build and validate pipeline definition
3. Trigger SageMaker pipeline in dev
4. Register model candidate
5. Promote to staging/prod after approval and checks

## 7) Minimal Execution Checklist

- [ ] Refactor local processing/training into SageMaker-compatible entry scripts
- [ ] Create SageMaker Pipeline definition
- [ ] Configure model registration and approval flow
- [ ] Add endpoint or batch deployment path
- [ ] Add monitoring + retraining trigger
- [ ] Document environment variables and runtime parameters

## 8) Suggested Runtime Parameters

- `random_state`
- `test_size`
- `training_instance_type`
- `processing_instance_type`
- `model_approval_status`
- `endpoint_instance_type`

## 9) Notes for This Portfolio Repo

- Keep local pipeline as the developer-fast path.
- Keep `sagemaker/` limited to job entrypoints; do not add AWS SDK packages to `requirements.txt` unless you explicitly choose to merge infra and modeling in one repo.
- Keep notebook usage demonstration-only; production logic remains in package scripts.
