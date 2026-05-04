from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PipelineConfig:
    random_state: int = 42
    n_users: int = 2000
    test_size: float = 0.25

    raw_data_path: Path = Path("data/raw/simulated_decision_data.csv")
    features_path: Path = Path("data/processed/features.csv")
    model_path: Path = Path("models/baseline_logreg.joblib")
    metrics_path: Path = Path("models/metrics.json")
