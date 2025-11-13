
import pandas as pd

def load_csv(filepath, ticker):
    """
    Load and clean a single asset CSV file.

    Reads a CSV containing columns ['Date', 'Close'] and adds
    a 'ticker' column for identification. Ensures the data is sorted
    by Date and formatted correctly.

    Parameters
    ----------
    filepath : str
        Path to the CSV file
    ticker : str
        Asset ticker

    Returns
    -------
    pd.DataFrame
        Clean DataFrame with columns ['Date', 'Close', 'ticker']
    """
    df = pd.read_csv(filepath)
    required_cols = {'Date', 'Close'}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"Missing required columns in {filepath}")

    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)
    df['ticker'] = ticker
    
    print(f"✅ {ticker} data loaded successfully with {len(df)} records.")

    return df


if __name__ == "__main__":
    v = load_csv('../data/V.csv', 'V')
    axp = load_csv('../data/AXP.csv', 'AXP')
    print(v.head(), axp.head())
