import numpy as np
import pandas as pd
import pytest
from commodity_analyser.indicator import add_indicators


def make_df(n=30):
    return pd.DataFrame({
        "date": pd.date_range("2024-01-01", periods=n),
        "price": np.arange(1.0, n + 1.0),
        "volume": np.ones(n) * 100,
    })


def test_columns_added():
    df = make_df()
    add_indicators(df, window=5)
    assert {"rolling_mean", "rolling_std", "zscore"}.issubset(df.columns)


def test_mutates_in_place():
    df = make_df()
    result = add_indicators(df, window=5)
    assert result is None
    assert "rolling_mean" in df.columns


def test_rolling_mean_values():
    df = make_df(10)
    add_indicators(df, window=3)
    # window=3: first valid index is 2 (0-based), value = mean(1,2,3) = 2.0
    assert df["rolling_mean"].iloc[2] == pytest.approx(2.0)


def test_rolling_std_values():
    df = make_df(10)
    add_indicators(df, window=3)
    expected_std = pd.Series([1.0, 2.0, 3.0]).std()
    assert df["rolling_std"].iloc[2] == pytest.approx(expected_std)


def test_zscore_values():
    df = make_df(10)
    add_indicators(df, window=3)
    # z-score at index 2: (3 - 2) / std([1,2,3])
    expected = (3.0 - 2.0) / pd.Series([1.0, 2.0, 3.0]).std()
    assert df["zscore"].iloc[2] == pytest.approx(expected)


def test_pre_window_rows_are_nan():
    df = make_df(10)
    add_indicators(df, window=5)
    assert df["rolling_mean"].iloc[:4].isna().all()
    assert df["zscore"].iloc[:4].isna().all()


def test_default_window_is_20():
    df = make_df(30)
    add_indicators(df)
    assert df["rolling_mean"].iloc[:19].isna().all()
    assert not pd.isna(df["rolling_mean"].iloc[19])


def test_invalid_window():
    df = make_df()
    with pytest.raises(ValueError, match="window must be at least 1"):
        add_indicators(df, window=0)
