from ..models.trading_algorithm import TradingAlgorithm
from .data_collection import collect_data
from .data_preprocessing import preprocess_data


def backtest(symbol, start_date, end_date, initial_capital=100000):
    # Collect and preprocess data
    raw_data = collect_data(symbol, start_date, end_date)
    data = preprocess_data(raw_data)
    
    algo = TradingAlgorithm()
    portfolio = initial_capital
    position = 0
    trades = []

    for index, row in data.iterrows():
        decision = algo.predict(row.to_dict())
        
        if decision in ["BUY", "STRONG_BUY"] and position == 0:
            position = portfolio / row['close']
            portfolio = 0
            trades.append(('BUY', index, row['close'], position))
        elif decision in ["SELL", "STRONG_SELL"] and position > 0:
            portfolio = position * row['close']
            position = 0
            trades.append(('SELL', index, row['close'], portfolio))
        
    final_portfolio = portfolio + position * data.iloc[-1]['close']
    return_pct = (final_portfolio - initial_capital) / initial_capital * 100
    
    return {
        'final_portfolio': final_portfolio,
        'return_pct': return_pct,
        'trades': trades
    }