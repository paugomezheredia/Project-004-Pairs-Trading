
import pandas as pd

def load_csv(filepath, ticker):
    """
    Load and clean a single asset CSV file.

    Reads a CSV containing columns ['date', 'adj_close'] and adds
    a 'ticker' column for identification. Ensures the data is sorted
    by date and formatted correctly.

    Parameters
    ----------
    filepath : str
        Path to the CSV file
    ticker : str
        Asset ticker

    Returns
    -------
    pd.DataFrame
        Clean DataFrame with columns ['date', 'adj_close', 'ticker']
    """
    df = pd.read_csv(filepath)
    required_cols = {'date', 'adj_close'}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"Missing required columns in {filepath}")

    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').reset_index(drop=True)
    df['ticker'] = ticker
    return df


if __name__ == "__main__":
    v = load_csv('../data/V.csv', 'V')
    ma = load_csv('../data/MA.csv', 'MA')
    print(v.head(), ma.head())
