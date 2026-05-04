from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import joblib
import pandas as pd


def _add_src_to_path() -> None:
    root = Path(__file__).resolve().parents[1]
    src_dir = root / "src"
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SageMaker training entrypoint.")
    parser.add_argument(
        "--train-data",
        type=str,
        default="/opt/ml/input/data/train/features.csv",
        help="Training feature CSV path.",
    )
    parser.add_argument(
        "--model-dir",
        type=str,
        default="/opt/ml/model",
        help="Directory where SageMaker expects model artifacts.",
    )
    parser.add_argument(
        "--metrics-path",
        type=str,
        default="/opt/ml/output/metrics.json",
        help="Path to write evaluation metrics JSON.",
    )
    parser.add_argument("--test-size", type=float, default=0.25, help="Test split ratio.")
    parser.add_argument("--random-state", type=int, default=42, help="Random seed.")
    return parser.parse_args()


def main() -> None:
    _add_src_to_path()
    from decision_engine.models.baseline import train_baseline_classifier

    args = parse_args()
    train_data_path = Path(args.train_data)
    model_dir = Path(args.model_dir)
    metrics_path = Path(args.metrics_path)

    model_dir.mkdir(parents=True, exist_ok=True)
    metrics_path.parent.mkdir(parents=True, exist_ok=True)

    feature_df = pd.read_csv(train_data_path)
    result = train_baseline_classifier(
        feature_df=feature_df,
        test_size=args.test_size,
        random_state=args.random_state,
    )

    model_output_path = model_dir / "model.joblib"
    joblib.dump(result.model, model_output_path)
    metrics_path.write_text(json.dumps(result.metrics, indent=2))

    print(f"Model written to: {model_output_path}")
    print(f"Metrics written to: {metrics_path}")


if __name__ == "__main__":
    main()
