from __future__ import annotations

import numpy as np
import pandas as pd


def _sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))


def generate_user_decision_data(n_users: int, random_state: int) -> pd.DataFrame:
    rng = np.random.default_rng(random_state)
    user_id = np.arange(1, n_users + 1)

    account_age_days = rng.integers(10, 3650, size=n_users)
    credit_score = np.clip(rng.normal(680, 80, size=n_users), 300, 850)
    tenure_months = np.clip(account_age_days // 30, 1, 120)

    transaction_count_30d = np.maximum(rng.poisson(18, size=n_users), 1)
    avg_transaction_amount = np.clip(rng.lognormal(mean=3.8, sigma=0.55, size=n_users), 8, 2000)
    chargeback_count_90d = rng.poisson(0.2, size=n_users)

    login_count_7d = np.maximum(rng.poisson(9, size=n_users), 1)
    failed_login_count_30d = rng.poisson(1.0, size=n_users)
    device_changes_30d = rng.poisson(0.7, size=n_users)

    risk_score = (
        -1.4
        + 0.003 * (700 - credit_score)
        + 0.09 * chargeback_count_90d
        + 0.13 * failed_login_count_30d
        + 0.2 * device_changes_30d
        + 0.007 * np.maximum(0, 10 - account_age_days / 365)
    )
    approval_probability = 1.0 - _sigmoid(risk_score)
    is_approved = rng.binomial(1, np.clip(approval_probability, 0.02, 0.98))

    return pd.DataFrame(
        {
            "user_id": user_id,
            "account_age_days": account_age_days,
            "tenure_months": tenure_months,
            "credit_score": credit_score.round(0).astype(int),
            "transaction_count_30d": transaction_count_30d,
            "avg_transaction_amount": avg_transaction_amount.round(2),
            "chargeback_count_90d": chargeback_count_90d,
            "login_count_7d": login_count_7d,
            "failed_login_count_30d": failed_login_count_30d,
            "device_changes_30d": device_changes_30d,
            "is_approved": is_approved.astype(int),
        }
    )
