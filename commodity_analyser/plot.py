import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def plot(df: pd.DataFrame, output: str) -> None:
    fig, ax = plt.subplots()
    ax.plot(df["date"], df["price"], label="Price")
    ax.plot(df["date"], df["rolling_mean"], label="Rolling Mean")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    fig.savefig(output)
    plt.close(fig)
