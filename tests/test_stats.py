import numpy as np
import pandas as pd
import pytest
from commodity_analyser.stats import compute_stats


def make_df(prices):
    return pd.DataFrame({
        "date": pd.date_range("2024-01-01", periods=len(prices)),
        "price": pd.Series(prices, dtype=float),
        "volume": np.ones(len(prices)) * 100,
    })


def test_returns_dict():
    result = compute_stats(make_df([1, 2, 3, 4, 5]))
    assert isinstance(result, dict)


def test_expected_keys():
    result = compute_stats(make_df([1, 2, 3, 4, 5]))
    assert set(result.keys()) == {"mean", "std", "min", "max", "p25", "p50", "p75"}


def test_mean():
    assert compute_stats(make_df([1, 2, 3, 4, 5]))["mean"] == pytest.approx(3.0)


def test_std():
    prices = [1, 2, 3, 4, 5]
    assert compute_stats(make_df(prices))["std"] == pytest.approx(pd.Series(prices, dtype=float).std())


def test_min_max():
    result = compute_stats(make_df([10, 3, 7, 1, 9]))
    assert result["min"] == pytest.approx(1.0)
    assert result["max"] == pytest.approx(10.0)


def test_percentiles():
    prices = list(range(1, 101))  # 1..100
    result = compute_stats(make_df(prices))
    assert result["p25"] == pytest.approx(25.75)
    assert result["p50"] == pytest.approx(50.5)
    assert result["p75"] == pytest.approx(75.25)


def test_single_row():
    result = compute_stats(make_df([42.0]))
    assert result["mean"] == pytest.approx(42.0)
    assert result["min"] == pytest.approx(42.0)
    assert result["max"] == pytest.approx(42.0)
