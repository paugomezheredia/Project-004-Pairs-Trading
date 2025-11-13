import numpy as np
import pandas as pd

class KalmanFilter:
    """
    Generic Kalman Filter implementation for sequential state estimation.
    Can be used to estimate dynamic hedge ratios or signal smoothing.
    """
    def __init__(self, F=1, H=1, Q=1e-5, R=1e-2, x0=0, P0=1):
        self.F = F  # State transition coefficient
        self.H = H  # Observation coefficient
        self.Q = Q  # Process noise covariance
        self.R = R  # Measurement noise covariance
        self.x = x0  # Initial state estimate
        self.P = P0  # Initial covariance estimate

    def update(self, z):
        """
        Perform a single predict-update step for observation z.
        """
        # Prediction
        x_pred = self.F * self.x
        P_pred = self.F * self.P * self.F + self.Q

        # Kalman gain
        K = P_pred * self.H / (self.H * P_pred * self.H + self.R)

        # Update
        self.x = x_pred + K * (z - self.H * x_pred)
        self.P = (1 - K * self.H) * P_pred

        return self.x, self.P, K

def kalman_hedge_ratio(df):
    """
    Estimate dynamic hedge ratios using Kalman Filter regression.
    """
    y = df['price_V'].values
    x = df['price_AXP'].values
    n = len(x)
    
    beta = np.zeros(n)
    kf = KalmanFilter(Q=1e-5, R=1e-2, x0=1, P0=1)

    for t in range(n):
        z = y[t] / (x[t] + 1e-8)
        beta[t], _, _ = kf.update(z)

    df['hedge_ratio'] = beta
    
    print("✅ Hedge ratio estimation complete.\n")

    return df

if __name__ == "__main__":
    df = pd.read_csv('../data/pairs_data.csv')
    df = kalman_hedge_ratio(df)
    print(df.head())
