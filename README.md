# Project-004-Pairs-Trading


## 📈 Project Overview

This project implements a Pairs Trading strategy using Visa (V) and Mastercard (MA) stock data. The pipeline automates every step — from data loading and cointegration testing to Kalman Filter–based dynamic hedge estimation, z-score computation, signal generation, and backtesting. By leveraging Engle-Granger and Johansen tests for statistical cointegration and applying state-space modeling through the Kalman Filter, the strategy dynamically adjusts hedge ratios to maintain market neutrality. The backtesting module incorporates realistic transaction costs and borrow rates, producing detailed performance metrics such as Sharpe Ratio, Sortino Ratio, total return, and maximum drawdown. This framework provides a complete foundation for testing and extending statistical arbitrage models in algorithmic trading research.


## ⚙️ Project Setup

### 1️⃣ Create Virtual Environment

To execute this project correctly we need to create a virtual envitonment (venv) and use the versions and libraries stated in the 'requirements.txt'. Use the following steps to do so:

- Create your venv locally:

    - for Mac / Linux users: python3 -m venv venv

    - for Windows users: py -m venv venv

### 2️⃣ Activate Environment

- Activate your venv:

    - for Mac / Linux users: source venv/bin/activate

    - for Windows users: .\venv\Scripts\Activate

💡 Tip: When activated, you’ll see '(venv)' at the beginning of your terminal line, which means you’re now working inside the virtual environment.

### 3️⃣ Install Dependencies

- Install 'requirements.txt':

    - for all OS users: pip install -r requirements.txt

## 🧠 Run the Experiment

### 4️⃣ Run Training Script

- Run Project from terminal:

    - for Mac / Linux users: python src/main.py

    - for Windows users: py src/main.py

As an outpur we obtain the metrics of the project's final results.
    
