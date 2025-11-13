"""
main.py
--------
Main orchestrator for the Pairs Trading project.

Executes the full pipeline:
1. Load Visa & Amex data
2. Merge and create pairs dataset
3. Perform cointegration tests
4. Estimate dynamic hedge ratios (Kalman Filter)
5. Compute spread and z-score
6. Generate trading signals
7. Run backtest simulation
8. Analyze performance and save figures
"""

import os
import sys
import pandas as pd
import numpy as np

# Ensure the current directory and parent directory are accessible
sys.path.append(os.path.dirname(__file__))

# === Import modules ===
from load_data import load_csv
from create_pairs_dataset import create_pairs_dataset
from initial_visualization import generate_pair_plots
from cointegration_tests import engle_granger_test, johansen_test
from kalman_filters import kalman_hedge_ratio
from trading_strategy import generate_signals
from backtesting import backtest
from performance_analysis import analyze_performance


def main():
    print("🚀 Starting Pairs Trading pipeline...\n")

    base_path = os.path.join(os.path.dirname(__file__), "..")
    data_path = os.path.join(base_path, "data")
    figures_path = os.path.join(base_path, "figures")
    os.makedirs(figures_path, exist_ok=True)

    # === LOAD RAW DATA ===
    print("📂 Loading Visa and Amex data...")
    v = load_csv(os.path.join(data_path, "V.csv"), "V")
    ma = load_csv(os.path.join(data_path, "AXP.csv"), "AXP")

    # === CREATE PAIRS DATASET ===
    print("🧩 Creating pairs dataset...")
    pairs_df = create_pairs_dataset(
        os.path.join(data_path, "V.csv"),
        os.path.join(data_path, "AXP.csv"),
        "V", "AXP",
        output_file=os.path.join(data_path, "pairs_data.csv"))
    
    # == INITIAL VISUALIZATION CHARTS ==
    base_path = os.path.join(os.path.dirname(__file__), "..")
    data_path = os.path.join(base_path, "data")
    figures_path = os.path.join(base_path, "figures")
    os.makedirs(figures_path, exist_ok=True)
    
    generate_pair_plots(data_path, figures_path)

    # === COINTEGRATION TESTS ===
    print("🔗 Running cointegration tests...")
    engle_result = engle_granger_test(pairs_df["spread"])
    johansen_result = johansen_test(pairs_df, ["price_V", "price_AXP"])

    # === DYNAMIC HEDGE RATIOS (KALMAN FILTER) ===
    print("🤖 Estimating dynamic hedge ratios with Kalman Filter...")
    pairs_df = kalman_hedge_ratio(pairs_df)

    # === COMPUTE SPREAD & Z-SCORE ===
    print("📊 Computing updated spread and z-score...")
    pairs_df["spread"] = pairs_df["price_V"] - pairs_df["hedge_ratio"] * pairs_df["price_AXP"]
    pairs_df["zscore"] = (pairs_df["spread"] - pairs_df["spread"].mean()) / pairs_df["spread"].std()
    pairs_df.to_csv(os.path.join(data_path, "pairs_data.csv"), index=False)

    # === TRADING SIGNALS ===
    print("💡 Generating trading signals...")
    pairs_df = generate_signals(pairs_df)

    # === BACKTEST STRATEGY ===
    print("🏁 Running backtest simulation...")
    results_df = backtest(pairs_df)

    # === PERFORMANCE ANALYSIS ===
    print("📈 Analyzing performance and saving figures...")
    results_file = os.path.join(data_path, "results.csv")

    if os.path.exists(results_file):
        df_results = pd.read_csv(results_file)
        analyze_performance(df_results)
    else:
        print("⚠️ Skipping performance analysis (results.csv not found).\n")

    print("🎯 Full Pairs Trading pipeline executed successfully!")


if __name__ == "__main__":
    main()
