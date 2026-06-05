import pytest
from click.testing import CliRunner
from commodity_analyser.cli import main


VALID_CSV = (
    "date,price,volume\n"
    "2024-01-01,100.0,500\n"
    "2024-01-02,102.5,600\n"
    "2024-01-03,101.0,550\n"
)


@pytest.fixture
def csv_file(tmp_path):
    p = tmp_path / "prices.csv"
    p.write_text(VALID_CSV)
    return str(p)


def test_happy_path(csv_file, tmp_path):
    output = str(tmp_path / "chart.png")
    result = CliRunner().invoke(main, [csv_file, "--window", "2", "--output", output])
    assert result.exit_code == 0
    assert "Price Statistics" in result.output
    assert "Mean:" in result.output
    assert f"Chart saved to {output}" in result.output
    assert (tmp_path / "chart.png").exists()


def test_invalid_csv_path(tmp_path):
    result = CliRunner().invoke(main, [str(tmp_path / "nonexistent.csv")])
    assert result.exit_code == 1
    assert "Error" in result.output


def test_invalid_window(csv_file, tmp_path):
    output = str(tmp_path / "chart.png")
    result = CliRunner().invoke(main, [csv_file, "--window", "0", "--output", output])
    assert result.exit_code == 1
    assert "window" in result.output


def test_non_integer_window(csv_file):
    result = CliRunner().invoke(main, [csv_file, "--window", "abc"])
    assert result.exit_code == 2
    assert "Error" in result.output


def test_csv_missing_columns(tmp_path):
    p = tmp_path / "bad.csv"
    p.write_text("date,close\n2024-01-01,100.0\n")
    result = CliRunner().invoke(main, [str(p)])
    assert result.exit_code == 1
    assert "missing required columns" in result.output
