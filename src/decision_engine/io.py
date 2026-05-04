from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import pandas as pd


def ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def save_dataframe(df: pd.DataFrame, path: Path) -> None:
    ensure_parent_dir(path)
    df.to_csv(path, index=False)


def load_dataframe(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def save_model(model: Any, path: Path) -> None:
    ensure_parent_dir(path)
    joblib.dump(model, path)


def save_metrics(metrics: dict[str, Any], path: Path) -> None:
    ensure_parent_dir(path)
    path.write_text(json.dumps(metrics, indent=2))
