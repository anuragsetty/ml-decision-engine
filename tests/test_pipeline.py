from __future__ import annotations

from pathlib import Path

from decision_engine.config import PipelineConfig
from decision_engine.pipeline import run_training_pipeline


def test_pipeline_writes_outputs(tmp_path: Path) -> None:
    config = PipelineConfig(
        n_users=150,
        random_state=7,
        test_size=0.2,
        raw_data_path=tmp_path / "raw.csv",
        features_path=tmp_path / "features.csv",
        model_path=tmp_path / "model.joblib",
        metrics_path=tmp_path / "metrics.json",
    )
    metrics = run_training_pipeline(config)
    assert "accuracy" in metrics
    assert "roc_auc" in metrics
    assert config.raw_data_path.exists()
    assert config.features_path.exists()
    assert config.model_path.exists()
    assert config.metrics_path.exists()
