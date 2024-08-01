import asyncio
import json

import pandas as pd
import websockets

from ..models.trading_algorithm import TradingAlgorithm
from .data_preprocessing import preprocess_data
from .database import store_in_elasticsearch, store_in_postgres


async def stream_market_data(symbol, interval='1m'):
    uri = f"wss://stream.binance.com:9443/ws/{symbol.lower()}@kline_{interval}"
    
    async with websockets.connect(uri) as websocket:
        while True:
            response = await websocket.recv()
            data = json.loads(response)
            
            kline = data['k']
            df = pd.DataFrame([{
                'open_time': kline['t'],
                'open': float(kline['o']),
                'high': float(kline['h']),
                'low': float(kline['l']),
                'close': float(kline['c']),
                'volume': float(kline['v']),
            }])
            
            processed_data = preprocess_data(df)
            
            # Store in databases
            store_in_postgres(processed_data, 'real_time_market_data')
            store_in_elasticsearch(processed_data, 'real_time_market_data')
            
            # Trigger trading algorithm
            algo = TradingAlgorithm()
            decision = algo.predict(processed_data.to_dict('records')[0])
            
            print(f"Symbol: {symbol}, Decision: {decision}")

def start_streaming(symbols):
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(stream_market_data(symbol)) for symbol in symbols]
    loop.run_until_complete(asyncio.wait(tasks))