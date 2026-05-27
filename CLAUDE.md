# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
poetry install

# Run all tests
poetry run pytest

# Run a single test file
poetry run pytest tests/test_loader.py

# Run a single test by name
poetry run pytest tests/test_indicators.py::test_rolling_mean

# Run the CLI
poetry run commodity-analyser <csv_path> --window 20 --output price_chart.png
```

## Architecture

The tool is a single-asset commodity price analyser with a linear pipeline:

1. **loader** — reads and validates a CSV (`date`, `price`, `volume` columns required), returns a `pd.DataFrame`
2. **stats** — computes summary statistics (mean, std, min, max, percentiles) on the `price` column
3. **indicators** — mutates the DataFrame in place, adding `rolling_mean`, `rolling_std`, and `zscore` columns using a configurable window
4. **plot** — renders a price series with rolling mean overlay and saves to disk
5. **cli** — `click` entrypoint that wires the pipeline together; accepts `csv_path`, `--window` (default 20), and `--output` (default `price_chart.png`)

Live data feeds, multi-asset analysis, and forecasting are explicitly out of scope per spec.
