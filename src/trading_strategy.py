import numpy as np
import pandas as pd

def generate_signals(df, entry_z=2.0, exit_z=0.5):
    """
    Generate trading signals based on z-score thresholds.

    Buy when z < -entry_z, sell when z > entry_z, exit when |z| < exit_z.
    """
    df['long_signal'] = (df['zscore'] < -entry_z).astype(int)
    df['short_signal'] = (df['zscore'] > entry_z).astype(int)
    df['exit_signal'] = (abs(df['zscore']) < exit_z).astype(int)
    print("✅ Trading signals generated.\n")
    return df

if __name__ == "__main__":
    df = pd.read_csv('../data/pairs_data.csv')
    df = generate_signals(df)
    print(df.head())
