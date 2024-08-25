import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

from stock_analysis import download_data, calculate_log_returns, calculate_covariance_matrix

x = st.slider('x', min_value=-50, max_value=50)  # 👈 this is a widget
st.write(x, 'squared is', x * x)

'''data = pd.read_csv("DAX40_2024.csv")
st.write(data)'''

df = pd.read_csv("DAX40.csv")


print(df['Ticker'])
tickers = df['Ticker']



end_date = datetime.today()
start_date = end_date - timedelta(days=20)

# st.write(optimize_weights(tickers=tickers, start_date=start_date, end_date=end_date, risk_free_rate=0.02))

adj_close_df = download_data(tickers, start_date, end_date)
log_returns = calculate_log_returns(adj_close_df)
cov_matrix = calculate_covariance_matrix(log_returns)

st.write(cov_matrix)

