import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt


def download_data(tickers, start_date, end_date):
    """Downloads historical price data for the specified tickers, skipping those not found."""
    adj_close_df = pd.DataFrame()
    skipped_tickers = []

    for ticker in tickers:
        try:
            data = yf.download(ticker, start=start_date, end=end_date)
            if data.empty:
                raise ValueError(f"No data found for {ticker}")
            adj_close_df[ticker] = data["Adj Close"]
        except Exception as e:
            print(f"Error downloading data for {ticker}: {e}")
            skipped_tickers.append(ticker)
    
    if skipped_tickers:
        print(f"Skipped tickers: {', '.join(skipped_tickers)}")
    
    return adj_close_df


def calculate_log_returns(adj_close_df):
    """Calculates the lognormal returns for each ticker."""
    log_returns = np.log(adj_close_df / adj_close_df.shift(1))
    return log_returns.dropna()


def calculate_covariance_matrix(log_returns):
    """Calculates the annualized covariance matrix."""
    return log_returns.cov() * 252


def standard_deviation(weights, cov_matrix):
    """Calculates the portfolio standard deviation."""
    variance = weights.T @ cov_matrix @ weights
    return np.sqrt(variance)


def expected_return(weights, log_returns):
    """Calculates the expected return of the portfolio."""
    return np.sum(weights * log_returns.mean()) * 252


def sharpe_ratio(weights, log_returns, cov_matrix, risk_free_rate):
    """Calculates the Sharpe ratio of the portfolio."""
    return (expected_return(weights, log_returns) - risk_free_rate) / standard_deviation(weights, cov_matrix)


def neg_sharpe_ratio(weights, log_returns, cov_matrix, risk_free_rate):
    """Returns the negative Sharpe ratio for optimization."""
    return -sharpe_ratio(weights, log_returns, cov_matrix, risk_free_rate)


def optimize_weights(tickers, start_date, end_date, risk_free_rate=0.02):
    """Optimizes the portfolio weights to maximize the Sharpe ratio."""
    adj_close_df = download_data(tickers, start_date, end_date)
    log_returns = calculate_log_returns(adj_close_df)
    cov_matrix = calculate_covariance_matrix(log_returns)
    initial_weights = np.array([1 / len(tickers)] * len(tickers))
    constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
    bounds = [(-2, 2) for _ in range(len(tickers))]

    optimized_results = minimize(neg_sharpe_ratio, initial_weights, args=(log_returns, cov_matrix, risk_free_rate),
                                  method='SLSQP', constraints=constraints, bounds=bounds)

    return optimized_results.x


def display_results(tickers, optimal_weights, start_date, end_date, risk_free_rate):
    """Prints the optimal weights, expected return, volatility, and Sharpe ratio."""
    print("Optimal Weights:")
    for ticker, weight in zip(tickers, optimal_weights):
        print(f"{ticker}: {weight:.4f}")

    adj_close_df = download_data(tickers, start_date, end_date)
    log_returns = calculate_log_returns(adj_close_df)
    cov_matrix = calculate_covariance_matrix(log_returns)
    optimal_portfolio_return = expected_return(optimal_weights, log_returns)
    optimal_portfolio_volatility = standard_deviation(optimal_weights, cov_matrix)
    optimal_sharpe_ratio = sharpe_ratio(optimal_weights, log_returns, cov_matrix, risk_free_rate)

    print(f"Expected Annual Return: {optimal_portfolio_return:.4f}")
    print(f"Expected Volatility: {optimal_portfolio_volatility:.4f}")
    print(f"Sharpe Ratio: {optimal_sharpe_ratio:.4f}")

    # Create a bar chart of the optimal weights
    plt.figure(figsize=(10, 6))
    plt.bar(tickers, optimal_weights)
    plt.xlabel("Assets")
    plt.ylabel("Optimal Weights")
    plt.title("Optimal Portfolio Weights")
    plt.show()



