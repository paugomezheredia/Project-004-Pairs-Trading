"""
initial_visualization.py

Generate and save two diagnostic charts for the pair:
  1) Price relationship (Visa vs Mastercard)
  2) Spread evolution (spread and rolling mean)

Behavior:
  - If data/pairs_data.csv exists, the script uses its columns (price_V, price_MA, spread).
  - Otherwise it falls back to reading data/V.csv and data/MA.csv and computes a simple static spread.
  - Saves figures to the 'figures' directory (creates it if missing).
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def generate_pair_plots(data_dir, figures_dir):
    """
    Generate and save price relationship and spread evolution plots.

    Parameters
    ----------
    data_dir : str
        Path to directory containing V.csv, MA.csv and optionally pairs_data.csv
    figures_dir : str
        Path where figures will be saved (directory will be created if needed)
    """
    print("📷 Generating pair diagnostic plots...")

    os.makedirs(figures_dir, exist_ok=True)

    pairs_path = os.path.join(data_dir, "pairs_data.csv")
    v_path = os.path.join(data_dir, "V.csv")
    ma_path = os.path.join(data_dir, "MA.csv")

    if os.path.exists(pairs_path):
        df = pd.read_csv(pairs_path, parse_dates=["date"])
        # Expecting price_V and price_MA columns; if not, try fallback
        if not {"price_V", "price_MA"}.issubset(df.columns):
            raise ValueError("pairs_data.csv found but missing price_V/price_MA columns.")
        price_v = df["price_V"]
        price_ma = df["price_MA"]
        spread = df["spread"] if "spread" in df.columns else (price_v - (price_v / price_ma).mean() * price_ma)
    else:
        # Fallback: load raw V and MA and merge by date
        if not (os.path.exists(v_path) and os.path.exists(ma_path)):
            raise FileNotFoundError("Neither pairs_data.csv nor V.csv/MA.csv found in data directory.")
        v = pd.read_csv(v_path, parse_dates=["date"])
        ma = pd.read_csv(ma_path, parse_dates=["date"])
        v = v.rename(columns={"adj_close": "price_V"})
        ma = ma.rename(columns={"adj_close": "price_MA"})
        merged = pd.merge(v[["date", "price_V"]], ma[["date", "price_MA"]], on="date", how="inner").sort_values("date")
        df = merged.reset_index(drop=True)
        price_v = df["price_V"]
        price_ma = df["price_MA"]
        # simple static beta (mean ratio)
        beta = (price_v / (price_ma + 1e-12)).mean()
        spread = price_v - beta * price_ma

    # Ensure date is datetime index for plotting
    if "date" in df.columns:
        dates = pd.to_datetime(df["date"])
    else:
        # If no date column, create index range
        dates = pd.RangeIndex(start=0, stop=len(df), step=1)

    # ---- Plot 1: Price relationship ----
    fig1, ax1 = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    ax1[0].plot(dates, price_v, label="Visa (V)")
    ax1[0].plot(dates, price_ma, label="Mastercard (MA)")
    ax1[0].set_title("Price Relationship: Visa vs Mastercard")
    ax1[0].set_ylabel("Adjusted Close Price")
    ax1[0].legend()
    ax1[0].grid(True)

    # Normalized comparison for clearer visual (base 100)
    norm_v = (price_v / price_v.iloc[0]) * 100 if len(price_v) > 0 else price_v
    norm_ma = (price_ma / price_ma.iloc[0]) * 100 if len(price_ma) > 0 else price_ma
    ax1[1].plot(dates, norm_v, label="Visa (base 100)")
    ax1[1].plot(dates, norm_ma, label="Mastercard (base 100)")
    ax1[1].set_title("Normalized Price (Base = 100)")
    ax1[1].set_ylabel("Indexed Price")
    ax1[1].set_xlabel("Date")
    ax1[1].legend()
    ax1[1].grid(True)

    fig1.tight_layout()
    price_relationship_file = os.path.join(figures_dir, "price_relationship.png")
    fig1.savefig(price_relationship_file)
    plt.close(fig1)
    print(f"✅ Saved price relationship plot to: {price_relationship_file}")

    # ---- Plot 2: Spread evolution ----
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.plot(dates, spread, label="Spread", linewidth=1)
    # Rolling mean to highlight slow changes:
    window = max(5, int(len(spread) * 0.05))  # 5% of data or at least 5 days
    rolling_mean = pd.Series(spread).rolling(window=window, min_periods=1, center=False).mean()
    ax2.plot(dates, rolling_mean, label=f"{window}-period Rolling Mean", color="orange", linewidth=1.5)
    ax2.axhline(0, color="gray", linestyle="--", linewidth=0.8)
    ax2.set_title("Spread Evolution")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Spread")
    ax2.legend()
    ax2.grid(True)

    fig2.tight_layout()
    spread_file = os.path.join(figures_dir, "spread_evolution.png")
    fig2.savefig(spread_file)
    plt.close(fig2)
    print(f"✅ Saved spread evolution plot to: {spread_file}")

    print("📷 Pair diagnostic plots generation completed.\n")


if __name__ == "__main__":
    # Example usage when run directly from src/
    base = os.path.join(os.path.dirname(__file__), "..")
    data_dir = os.path.join(base, "data")
    figures_dir = os.path.join(base, "figures")
    generate_pair_plots(data_dir, figures_dir)
