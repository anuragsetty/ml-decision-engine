from __future__ import annotations

import argparse
import json

from decision_engine.config import PipelineConfig
from decision_engine.pipeline import run_training_pipeline


def _build_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run decision engine training pipeline.")
    parser.add_argument("--n-users", type=int, default=2000, help="Number of simulated users.")
    parser.add_argument("--random-state", type=int, default=42, help="Random seed.")
    parser.add_argument("--test-size", type=float, default=0.25, help="Test set ratio.")
    return parser.parse_args()


def main() -> None:
    args = _build_args()
    config = PipelineConfig(
        n_users=args.n_users,
        random_state=args.random_state,
        test_size=args.test_size,
    )
    metrics = run_training_pipeline(config)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
