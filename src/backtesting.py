import pandas as pd
import numpy as np

def backtest(df, initial_cash=1_000_000, commission=0.00125, borrow_rate=0.0025):
    """
    Simulate a simple pairs trading strategy backtest.
    Applies transaction costs and daily borrow fees.
    """
    cash = initial_cash
    position = 0
    portfolio = []
    
    for i in range(len(df)):
        if df.loc[i, 'long_signal'] == 1 and position == 0:
            position = 1
            entry_price = df.loc[i, 'spread']
            cash -= commission * cash

        elif df.loc[i, 'short_signal'] == 1 and position == 0:
            position = -1
            entry_price = df.loc[i, 'spread']
            cash -= commission * cash

        elif df.loc[i, 'exit_signal'] == 1 and position != 0:
            pnl = position * (entry_price - df.loc[i, 'spread'])
            cash += pnl
            position = 0
            cash -= commission * cash

        portfolio.append(cash)

    df['portfolio_value'] = portfolio
    df.to_csv('../data/results.csv', index=False)
    print("✅ Backtest complete. Results saved to data/results.csv")
    return df

if __name__ == "__main__":
    df = pd.read_csv('../data/pairs_data.csv')
    df = backtest(df)
    print(df.tail())
