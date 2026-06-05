import io
import pytest
import pandas as pd
from commodity_analyser.data import load_csv


VALID_CSV = "date,price,volume\n2024-01-01,100.0,500\n2024-01-02,102.5,600\n"


@pytest.fixture
def csv_file(tmp_path):
    def _write(content, filename="data.csv"):
        p = tmp_path / filename
        p.write_text(content)
        return str(p)
    return _write


def test_valid_input(csv_file):
    df = load_csv(csv_file(VALID_CSV))
    assert list(df.columns) == ["date", "price", "volume"]
    assert pd.api.types.is_datetime64_any_dtype(df["date"])
    assert len(df) == 2
    assert df["price"].iloc[0] == 100.0


def test_missing_columns(csv_file):
    csv = "date,close\n2024-01-01,100.0\n"
    with pytest.raises(ValueError, match="missing required columns"):
        load_csv(csv_file(csv))


def test_non_numeric_price(csv_file):
    csv = "date,price,volume\n2024-01-01,abc,500\n2024-01-02,102.5,600\n"
    with pytest.raises(ValueError, match="'price' must be numeric"):
        load_csv(csv_file(csv))


def test_non_numeric_volume(csv_file):
    csv = "date,price,volume\n2024-01-01,100.0,lots\n2024-01-02,102.5,600\n"
    with pytest.raises(ValueError, match="'volume' must be numeric"):
        load_csv(csv_file(csv))
