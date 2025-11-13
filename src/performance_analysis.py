import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def analyze_performance(df):
    """
    Compute performance metrics, generate performance plots, 
    and save them in a 'figures' directory.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing 'date' and 'portfolio_value' columns.

    Returns
    -------
    None
        Saves plots and prints summary statistics.
    """
    print("🔍 Starting performance analysis...")

    os.makedirs('figures', exist_ok=True)

    df['returns'] = df['portfolio_value'].pct_change().fillna(0)

    # Basic performance metrics
    sharpe = np.mean(df['returns']) / np.std(df['returns']) * np.sqrt(252)
    sortino = np.mean(df['returns']) / np.std(df.loc[df['returns'] < 0, 'returns']) * np.sqrt(252)
    max_dd = (df['portfolio_value'].cummax() - df['portfolio_value']).max()
    total_return = df['portfolio_value'].iloc[-1] / df['portfolio_value'].iloc[0] - 1

    print(f"📈 Sharpe Ratio: {sharpe:.2f}")
    print(f"⚙️ Sortino Ratio: {sortino:.2f}")
    print(f"💰 Total Return: {total_return:.2%}")
    print(f"📉 Max Drawdown: {max_dd:.2f}")

    # ------- Equity Curve -------
    plt.figure(figsize=(10, 5))
    plt.plot(df['date'], df['portfolio_value'], color='blue')
    plt.title("Equity Curve Over Time")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('figures/equity_curve.png')
    plt.close()

    # ------- Daily Returns Distribution -------
    plt.figure(figsize=(8, 5))
    plt.hist(df['returns'], bins=50, color='steelblue', edgecolor='black', alpha=0.7)
    plt.title("Distribution of Daily Returns")
    plt.xlabel("Daily Return")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig('figures/returns_distribution.png')
    plt.close()

    # ------- Rolling Sharpe Ratio -------
    rolling_window = 60
    rolling_sharpe = (df['returns'].rolling(rolling_window).mean() /
                      df['returns'].rolling(rolling_window).std()) * np.sqrt(252)
    plt.figure(figsize=(10, 5))
    plt.plot(df['date'], rolling_sharpe, color='darkorange')
    plt.title(f"Rolling {rolling_window}-Day Sharpe Ratio")
    plt.xlabel("Date")
    plt.ylabel("Sharpe Ratio")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('figures/rolling_sharpe.png')
    plt.close()

    # ------- Drawdown Curve -------
    cumulative_max = df['portfolio_value'].cummax()
    drawdown = (df['portfolio_value'] - cumulative_max) / cumulative_max
    plt.figure(figsize=(10, 5))
    plt.plot(df['date'], drawdown, color='red')
    plt.title("Drawdown Over Time")
    plt.xlabel("Date")
    plt.ylabel("Drawdown")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('figures/drawdown_curve.png')
    plt.close()

    print("✅ Performance analysis complete. All plots saved to 'figures/' folder.")


if __name__ == "__main__":
    df = pd.read_csv('../data/results.csv')
    analyze_performance(df)
