"""The frozen, outcome-free mailing recommendation rule."""
import math
import pandas as pd


def high_history_policy(history: pd.Series, capacity_fraction: float = 10_000 / 64_000) -> pd.Series:
    """Recommend Mens to the largest histories, with input-order tie breaking.

    The index locates analysis records; it is not asserted to identify people.
    This function returns recommendations and does not send email.
    """
    if not 0 <= capacity_fraction <= 1:
        raise ValueError("capacity_fraction must be between zero and one")
    if not history.index.is_unique:
        raise ValueError("Use a unique analysis-record index")
    if history.isna().any():
        raise ValueError("history must not contain missing values")
    capacity = math.floor(len(history) * capacity_fraction)
    policy = pd.Series("No E-Mail", index=history.index, dtype=object)
    policy.loc[history.nlargest(capacity, keep="first").index] = "Mens E-Mail"
    return policy
