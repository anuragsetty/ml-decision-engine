from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

TARGET = "is_approved"
DROP_COLUMNS = ["user_id"]


@dataclass
class TrainingResult:
    model: Pipeline
    metrics: dict[str, Any]


def train_baseline_classifier(
    feature_df: pd.DataFrame, test_size: float, random_state: int
) -> TrainingResult:
    X = feature_df.drop(columns=DROP_COLUMNS + [TARGET], errors="ignore")
    y = feature_df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        stratify=y,
        random_state=random_state,
    )

    model = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=2000)),
        ]
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:, 1]
    metrics = {
        "accuracy": float(accuracy_score(y_test, preds)),
        "roc_auc": float(roc_auc_score(y_test, probs)),
        "classification_report": classification_report(y_test, preds, output_dict=True),
    }
    return TrainingResult(model=model, metrics=metrics)
