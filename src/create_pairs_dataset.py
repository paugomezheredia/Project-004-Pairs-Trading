import pandas as pd
from load_data import load_csv

def create_pairs_dataset(file_a, file_b, ticker_a, ticker_b, output_file='../data/pairs_data.csv'):
    """
    Combine two single-asset datasets into a unified pairs dataset.

    Merges both assets by date, computes spread and z-score, and
    saves the resulting file for further analysis.

    Parameters
    ----------
    file_a, file_b : str
        Paths to the two input CSV files
    ticker_a, ticker_b : str
        Asset tickers
    output_file : str
        Path to save merged dataset

    Returns
    -------
    pd.DataFrame
        Merged dataset containing prices, spread, and zscore
    """
    df_a = load_csv(file_a, ticker_a)
    df_b = load_csv(file_b, ticker_b)

    df_a.rename(columns={'adj_close': f'price_{ticker_a}'}, inplace=True)
    df_b.rename(columns={'adj_close': f'price_{ticker_b}'}, inplace=True)

    merged = pd.merge(df_a[['date', f'price_{ticker_a}']],
                      df_b[['date', f'price_{ticker_b}']],
                      on='date', how='inner')

    merged['ticker_A'] = ticker_a
    merged['ticker_B'] = ticker_b

    beta = (merged[f'price_{ticker_a}'] / merged[f'price_{ticker_b}']).mean()
    merged['spread'] = merged[f'price_{ticker_a}'] - beta * merged[f'price_{ticker_b}']
    merged['zscore'] = (merged['spread'] - merged['spread'].mean()) / merged['spread'].std()

    merged.to_csv(output_file, index=False)

    print(f"✅ Pairs dataset saved: {output_file}")
    
    return merged


if __name__ == "__main__":
    create_pairs_dataset('../data/V.csv', '../data/MA.csv', 'V', 'MA')
