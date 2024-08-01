import os

import numpy as np
import pandas as pd
import quandl
import yfinance as yf
from alpha_vantage.timeseries import TimeSeries
from dotenv import load_dotenv
from sklearn.preprocessing import StandardScaler

load_dotenv()

ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
QUANDL_API_KEY = os.getenv('QUANDL_API_KEY')

def get_alpha_vantage_data(symbol, interval='1min'):
    ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format='pandas')
    data, _ = ts.get_intraday(symbol=symbol, interval=interval, outputsize='full')
    return data

def get_yahoo_finance_data(symbol, start_date, end_date):
    ticker = yf.Ticker(symbol)
    data = ticker.history(start=start_date, end=end_date)
    return data

def get_quandl_data(dataset_code, start_date, end_date):
    quandl.ApiConfig.api_key = QUANDL_API_KEY
    data = quandl.get(dataset_code, start_date=start_date, end_date=end_date)
    return data

def collect_data(symbol, start_date, end_date):
    av_data = get_alpha_vantage_data(symbol)
    yf_data = get_yahoo_finance_data(symbol, start_date, end_date)
    quandl_data = get_quandl_data(f'WIKI/{symbol}', start_date, end_date)
    
    # Combine and process the data as needed
    combined_data = av_data.join(yf_data, how='outer').join(quandl_data, how='outer')
    
    return combined_data

def preprocess_data(data):
    if isinstance(data, str):
        # Assume it's a file path
        data = pd.read_csv(data)
    elif isinstance(data, dict):
        # Assume it's already a dictionary
        data = pd.DataFrame(data)
    
    # Data cleaning steps
    data = data.dropna()
    
    # Feature engineering
    data['return'] = data['close'].pct_change()
    data['log_return'] = np.log(data['close'] / data['close'].shift(1))
    data['volatility'] = data['log_return'].rolling(window=20).std() * np.sqrt(252)
    data['sma_20'] = data['close'].rolling(window=20).mean()
    data['sma_50'] = data['close'].rolling(window=50).mean()
    data['rsi'] = calculate_rsi(data['close'])
    
    # Scaling features
    scaler = StandardScaler()
    features = ['open', 'high', 'low', 'close', 'volume', 'return', 'log_return', 'volatility', 'sma_20', 'sma_50', 'rsi']
    data[features] = scaler.fit_transform(data[features])
    
    return data

def calculate_rsi(prices, period=14):
    delta = prices.diff()