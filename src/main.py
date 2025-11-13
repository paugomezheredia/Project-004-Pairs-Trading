"""
main.py
--------
Master script to execute the full Pairs Trading project pipeline.

This script sequentially runs all modules:
    1. Load and merge raw data (Visa & Mastercard)
    2. Run cointegration tests
    3. Estimate dynamic hedge ratios with Kalman filters
    4. Generate trading signals
    5. Perform backtesting with transaction costs
    6. Analyze performance and generate figures

All intermediate data and results are stored in the /data and /figures folders.
"""

import sys
import pandas as pd

# Import all project modules
from create_pairs_dataset import create_pairs_dataset
from cointegration_tests import run_cointegration_tests
from kalman_filters import run_kalman_filters
from trading_strategy import generate_trading_signals
from backtesting import backtest_strategy
from performance_analysis import analyze_performance

def main():
    """Run all stages of the Pairs Trading pipeline sequentially."""
    print("🚀 Starting full Pairs Trading pipeline...\n")

    try:
        # 1️⃣ Merge both datasets into one clean file
        print("🧩 Step 1: Creating merged dataset...")
        create_pairs_dataset('data/V.csv', 'data/MA.csv', output_file='data/pairs_data.csv')

        # 2️⃣ Run cointegration tests
        print("\n🔗 Step 2: Running cointegration tests...")
        run_cointegration_tests('data/pairs_data.csv')

        # 3️⃣ Estimate hedge ratios with Kalman filters
        print("\n📉 Step 3: Running Kalman filters...")
        run_kalman_filters('data/pairs_data.csv')

        # 4️⃣ Generate trading signals
        print("\n⚙️ Step 4: Generating trading signals...")
        generate_trading_signals('data/pairs_data.csv')

        # 5️⃣ Backtest the trading strategy
        print("\n💰 Step 5: Running backtest...")
        backtest_strategy('data/pairs_data.csv', output_file='data/results.csv')

        # 6️⃣ Analyze performance and save figures
        print("\n📊 Step 6: Analyzing performance...")
        df = pd.read_csv('data/results.csv')
        analyze_performance(df)

        print("\n✅ All steps completed successfully. Results saved in /data and /figures folders.")
    
    except Exception as e:
        print(f"❌ Pipeline stopped due to an error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
