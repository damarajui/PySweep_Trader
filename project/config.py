import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
    QUANDL_API_KEY = os.getenv('QUANDL_API_KEY')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    ELASTICSEARCH_HOST = os.getenv('ELASTICSEARCH_HOST')
    MODEL_PATH = './saved_models/latest/pytorch_model.bin'
    TRADING_SYMBOLS = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']
    HISTORICAL_DATA_START = '2010-01-01'
    HISTORICAL_DATA_END = '2023-05-01'
    REAL_TIME_DATA_INTERVAL = '1min'