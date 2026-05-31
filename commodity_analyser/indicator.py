import pandas as pd


def add_indicators(df: pd.DataFrame, window: int = 20) -> None:
    if window < 1:
        raise ValueError(f"window must be at least 1, got {window}")

    df["rolling_mean"] = df["price"].rolling(window).mean()
    df["rolling_std"] = df["price"].rolling(window).std()
    df["zscore"] = (df["price"] - df["rolling_mean"]) / df["rolling_std"]
