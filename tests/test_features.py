from __future__ import annotations

import pandas as pd

from decision_engine.features.transform import build_feature_table


def test_feature_engineering_adds_expected_columns() -> None:
    df = pd.DataFrame(
        {
            "user_id": [1, 2],
            "account_age_days": [100, 500],
            "tenure_months": [3, 16],
            "credit_score": [620, 740],
            "transaction_count_30d": [10, 20],
            "avg_transaction_amount": [100.0, 50.0],
            "chargeback_count_90d": [1, 0],
            "login_count_7d": [8, 10],
            "failed_login_count_30d": [2, 1],
            "device_changes_30d": [1, 0],
            "is_approved": [0, 1],
        }
    )
    features = build_feature_table(df)
    for col in [
        "chargeback_rate",
        "failed_login_rate",
        "txn_volume_30d",
        "account_age_years",
        "credit_score_normalized",
        "behavior_risk_index",
    ]:
        assert col in features.columns
