from __future__ import annotations

import numpy as np
import pandas as pd


def build_feature_table(raw_df: pd.DataFrame) -> pd.DataFrame:
    df = raw_df.copy()
    df["chargeback_rate"] = (df["chargeback_count_90d"] / df["transaction_count_30d"]).clip(0, 1)
    df["failed_login_rate"] = (df["failed_login_count_30d"] / (df["login_count_7d"] * 4)).clip(0, 1)
    df["txn_volume_30d"] = df["transaction_count_30d"] * df["avg_transaction_amount"]
    df["account_age_years"] = df["account_age_days"] / 365.0
    df["credit_score_normalized"] = (df["credit_score"] - 300) / 550
    df["behavior_risk_index"] = (
        0.5 * df["failed_login_rate"]
        + 0.35 * df["chargeback_rate"]
        + 0.15 * np.minimum(df["device_changes_30d"] / 5, 1)
    )
    return df
