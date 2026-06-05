import pandas as pd


def compute_stats(df: pd.DataFrame) -> dict:
    price = df["price"]
    return {
        "mean": price.mean(),
        "std": price.std(),
        "min": price.min(),
        "max": price.max(),
        "p25": price.quantile(0.25),
        "p50": price.quantile(0.50),
        "p75": price.quantile(0.75),
    }
