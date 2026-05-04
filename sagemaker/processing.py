from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd


def _add_src_to_path() -> None:
    root = Path(__file__).resolve().parents[1]
    src_dir = root / "src"
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="SageMaker processing step for feature generation."
    )
    parser.add_argument(
        "--input-data",
        type=str,
        default="/opt/ml/processing/input/simulated_decision_data.csv",
        help="Raw CSV input path.",
    )
    parser.add_argument(
        "--output-data",
        type=str,
        default="/opt/ml/processing/output/features.csv",
        help="Processed feature CSV output path.",
    )
    return parser.parse_args()


def main() -> None:
    _add_src_to_path()
    from decision_engine.features.transform import build_feature_table

    args = parse_args()
    input_path = Path(args.input_data)
    output_path = Path(args.output_data)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    raw_df = pd.read_csv(input_path)
    feature_df = build_feature_table(raw_df)
    feature_df.to_csv(output_path, index=False)
    print(f"Wrote features to: {output_path}")


if __name__ == "__main__":
    main()
