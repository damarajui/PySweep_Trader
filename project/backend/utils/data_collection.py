import os

import quandl
import yfinance as yf
from alpha_vantage.timeseries import TimeSeries
from dotenv import load_dotenv

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