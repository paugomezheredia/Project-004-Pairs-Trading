"""
initial_visualization.py

Generate and save two diagnostic charts for the pair:
  1) Price relationship (Visa vs Amex)
  2) Spread evolution (spread and rolling mean)

Behavior:
  - If data/pairs_data.csv exists, the script uses its columns (price_V, price_AXP, spread).
  - Otherwise it falls back to reading data/V.csv and data/AXP.csv and computes a simple static spread.
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
        Path to directory containing V.csv, AXP.csv and optionally pairs_data.csv
    figures_dir : str
        Path where figures will be saved (directory will be created if needed)
    """
    print("📷 Generating pair diagnostic plots...")

    os.makedirs(figures_dir, exist_ok=True)

    pairs_path = os.path.join(data_dir, "pairs_data.csv")
    v_path = os.path.join(data_dir, "V.csv")
    axp_path = os.path.join(data_dir, "AXP.csv")

    if os.path.exists(pairs_path):
        df = pd.read_csv(pairs_path, parse_dates=["Date"])
        # Expecting price_V and price_AXP columns; if not, try fallback
        if not {"price_V", "price_AXP"}.issubset(df.columns):
            raise ValueError("pairs_data.csv found but missing price_V/price_AXP columns.")
        price_v = df["price_V"]
        price_AXP = df["price_AXP"]
        spread = df["spread"] if "spread" in df.columns else (price_v - (price_v / price_AXP).mean() * price_AXP)
    else:
        # Fallback: load raw V and AXP and merge by date
        if not (os.path.exists(v_path) and os.path.exists(axp_path)):
            raise FileNotFoundError("Neither pairs_data.csv nor V.csv/AXP.csv found in data directory.")
        v = pd.read_csv(v_path, parse_dates=["Date"])
        axp = pd.read_csv(axp_path, parse_dates=["Date"])
        v = v.rename(columns={"Close": "price_V"})
        axp = axp.rename(columns={"Close": "price_AXP"})
        merged = pd.merge(v[["Date", "price_V"]], axp[["Date", "price_AXP"]], on="Date", how="inner").sort_values("Date")
        df = merged.reset_index(drop=True)
        price_v = df["price_V"]
        price_AXP = df["price_AXP"]
        # simple static beta (mean ratio)
        beta = (price_v / (price_AXP + 1e-12)).mean()
        spread = price_v - beta * price_AXP

    # Ensure date is datetime index for plotting
    if "Date" in df.columns:
        dates = pd.to_datetime(df["Date"])
    else:
        # If no date column, create index range
        dates = pd.RangeIndex(start=0, stop=len(df), step=1)

    # ---- Plot 1: Price relationship ----
    fig1, ax1 = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    ax1[0].plot(dates, price_v, label="Visa (V)")
    ax1[0].plot(dates, price_AXP, label="Amex (AXP)")
    ax1[0].set_title("Price Relationship: Visa vs Amex")
    ax1[0].set_ylabel("Adjusted Close Price")
    ax1[0].legend()
    ax1[0].grid(True)

    # Normalized comparison for clearer visual (base 100)
    norm_v = (price_v / price_v.iloc[0]) * 100 if len(price_v) > 0 else price_v
    norm_axp = (price_AXP / price_AXP.iloc[0]) * 100 if len(price_AXP) > 0 else price_AXP
    ax1[1].plot(dates, norm_v, label="Visa (base 100)")
    ax1[1].plot(dates, norm_axp, label="Amex (base 100)")
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
