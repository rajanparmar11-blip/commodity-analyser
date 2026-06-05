import click
from commodity_analyser.data import load_csv
from commodity_analyser.stats import compute_stats
from commodity_analyser.indicator import add_indicators
from commodity_analyser.plot import plot


@click.command()
@click.argument("csv_path")
@click.option("--window", default=20, show_default=True, type=int, help="Rolling window size.")
@click.option("--output", default="price_chart.png", show_default=True, help="Output path for the chart.")
def main(csv_path: str, window: int, output: str) -> None:
    try:
        df = load_csv(csv_path)
        stats = compute_stats(df)
        click.echo("Price Statistics")
        click.echo(f"  Mean:   {stats['mean']:.4f}")
        click.echo(f"  Std:    {stats['std']:.4f}")
        click.echo(f"  Min:    {stats['min']:.4f}")
        click.echo(f"  Max:    {stats['max']:.4f}")
        click.echo(f"  P25:    {stats['p25']:.4f}")
        click.echo(f"  P50:    {stats['p50']:.4f}")
        click.echo(f"  P75:    {stats['p75']:.4f}")
        add_indicators(df, window=window)
        plot(df, output)
    except (ValueError, FileNotFoundError) as exc:
        raise click.ClickException(str(exc))
    click.echo(f"Chart saved to {output}")
