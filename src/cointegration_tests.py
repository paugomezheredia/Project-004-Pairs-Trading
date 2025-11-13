import pandas as pd
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.vector_ar.vecm import coint_johansen

def engle_granger_test(spread):
    """
    Perform Engle-Granger ADF test for cointegration.

    Parameters
    ----------
    spread : pd.Series
        Residuals or spread between two assets

    Returns
    -------
    dict
        Test statistic and p-value
    """
    print("Running Engle-Granger ADF test...")
    print("✅ Engle-Granger ADF test completed.")
    result = adfuller(spread)
    print(f"ADF Statistic: {result[0]:.4f}, p-value: {result[1]:.4f}")
    return {'ADF Statistic': result[0],
            'p-value': result[1],
            'Critical Values': result[4]}

def johansen_test(df, cols):
    """
    Run Johansen cointegration test.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing both price series
    cols : list
        List of column names to test (e.g., ['price_V', 'price_MA'])

    Returns
    -------
    dict
        Eigenvalues and trace statistics
    """
    print("\nRunning Johansen cointegration test...")
    result = coint_johansen(df[cols], det_order=0, k_ar_diff=1)
    print("✅ Johansen test completed.")
    print("Eigenvalues:", result.eig)
    return {'Eigenvalues': result.eig,
            'Trace Statistics': result.lr1,
            'Critical Values (90%,95%,99%)': result.cvt}


if __name__ == "__main__":
    df = pd.read_csv('../data/pairs_data.csv')
    print(engle_granger_test(df['spread']))
    print(johansen_test(df, ['price_V', 'price_MA']))
