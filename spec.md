# Commodity Price Analyser

## Purpose
CLI tool to load commodity price time series, compute summary statistics
and basic technical indicators, and plot results.

## Inputs
- CSV with columns: date, price, volume

## Features
- Load and validate data
- Summary stats: mean, std, min/max, percentiles
- Indicators: rolling mean, rolling std, z-score
- Plot: price series with rolling mean overlay

## Out of scope
- Live data feeds
- Multiple assets simultaneously
- Forecasting

## Stack
- Python 3.11
- pandas, NumPy, matplotlib
- pytest for tests
- click for CLI
- Poetry for dependency management

## Done when
- CLI accepts a CSV path and window size
- Outputs stats to terminal
- Saves a plot to disk
- Tests cover data loading and indicator calculations
