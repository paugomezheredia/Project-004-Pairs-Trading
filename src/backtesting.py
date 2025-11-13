import os
import pandas as pd
import numpy as np

def backtest(df, initial_cash=1_000_000, commission=0.00125, borrow_rate=0.0025, output_path=None):
    """
    Simulate a simple pairs trading strategy backtest.
    Applies transaction costs and daily borrow fees.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing price data and trading signals.
    initial_cash : float, default=1_000_000
        Starting portfolio value.
    commission : float, default=0.00125
        Transaction cost percentage per trade.
    borrow_rate : float, default=0.0025
        Daily short borrow rate.
    output_path : str or None
        Custom file path to save results (optional).

    Returns
    -------
    pd.DataFrame
        DataFrame with simulated portfolio values.
    """
    # === Define safe output path early ===
    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), "..", "data", "results.csv")

    # === Ensure output directory exists ===
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    cash = initial_cash
    position = 0
    portfolio = []

    for i in range(len(df)):
        if df.loc[i, 'long_signal'] == 1 and position == 0:
            position = 1
            entry_price = df.loc[i, 'spread']
            cash -= commission * cash  # transaction cost

        elif df.loc[i, 'short_signal'] == 1 and position == 0:
            position = -1
            entry_price = df.loc[i, 'spread']
            cash -= commission * cash  # transaction cost

        elif df.loc[i, 'exit_signal'] == 1 and position != 0:
            pnl = position * (entry_price - df.loc[i, 'spread'])
            cash += pnl
            position = 0
            cash -= commission * cash  # transaction cost

        # Apply daily borrow fee if short
        if position == -1:
            cash -= borrow_rate * cash / 252  # approximate daily rate

        portfolio.append(cash)

    df['portfolio_value'] = portfolio

    # === Save results ===
    df.to_csv(output_path, index=False)
    print(f"✅ Backtest complete. Results saved to {output_path}")

    return df


if __name__ == "__main__":
    # Test run when executed directly
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "pairs_data.csv")
    df = pd.read_csv(data_path)
    df = backtest(df)
    print(df.tail())
