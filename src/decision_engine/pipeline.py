from __future__ import annotations

from decision_engine.config import PipelineConfig
from decision_engine.data.simulator import generate_user_decision_data
from decision_engine.features.transform import build_feature_table
from decision_engine.io import save_dataframe, save_metrics, save_model
from decision_engine.models.baseline import train_baseline_classifier


def run_training_pipeline(config: PipelineConfig | None = None) -> dict:
    cfg = config or PipelineConfig()

    raw_df = generate_user_decision_data(n_users=cfg.n_users, random_state=cfg.random_state)
    save_dataframe(raw_df, cfg.raw_data_path)

    feature_df = build_feature_table(raw_df)
    save_dataframe(feature_df, cfg.features_path)

    result = train_baseline_classifier(
        feature_df=feature_df,
        test_size=cfg.test_size,
        random_state=cfg.random_state,
    )
    save_model(result.model, cfg.model_path)
    save_metrics(result.metrics, cfg.metrics_path)
    return result.metrics
