# Contributing

## Development Setup

```bash
make setup
```

## Quality Checks

Run before opening a PR:

```bash
.venv/bin/python -m black src tests sagemaker
.venv/bin/python -m ruff check src tests sagemaker
.venv/bin/python -m pytest -q
```

## Contribution Principles

- Keep pipeline logic in `src/decision_engine/`.
- Keep notebooks focused on analysis and visualization.
- Add tests for non-trivial logic changes.
- Update `docs/model_card.md` when model behavior changes.
- Do not add AWS SDK packages (`boto3`, `sagemaker`, etc.) to `requirements.txt` unless the project explicitly adopts that dependency; keep SageMaker pipeline and infra code outside this repo when possible.
