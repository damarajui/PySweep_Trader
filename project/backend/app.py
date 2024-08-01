import pandas as pd
from flask import Flask, jsonify, request
from models.trading_algorithm import TradingAlgorithm
from utils.backtesting import backtest
from utils.data_collection import collect_data
from utils.data_preprocessing import preprocess_data
from utils.data_streaming import start_streaming
from utils.database import store_in_elasticsearch, store_in_postgres
from utils.file_handling import get_file_content, save_uploaded_file
from utils.logging_config import logger

app = Flask(__name__)

@app.route('/trade', methods=['POST'])
def trade():
    try:
        data = request.json
        algo = TradingAlgorithm()
        decision = algo.predict(data)
        logger.info(f"Trade decision: {decision}")
        return jsonify({'decision': decision})
    except Exception as e:
        logger.error(f"Error in trade route: {str(e)}", exc_info=True)
        return jsonify({"error": "An error occurred while processing the trade"}), 500

@app.route('/collect_data', methods=['GET'])
def get_data():
    symbol = request.args.get('symbol', default='AAPL', type=str)
    start_date = request.args.get('start_date', default='2023-01-01', type=str)
    end_date = request.args.get('end_date', default='2023-12-31', type=str)
    
    raw_data = collect_data(symbol, start_date, end_date)
    processed_data = preprocess_data(raw_data)
    
    # Store data in PostgreSQL and Elasticsearch
    store_in_postgres(processed_data, 'market_data')
    store_in_elasticsearch(processed_data, 'market_data')
    
    return jsonify(processed_data.to_dict())

@app.route('/train_model', methods=['POST'])
def train_model():
    from ai_ml.train import main as train_main
    try:
        train_main()
        return jsonify({'message': 'Model trained successfully'}), 200
    except Exception as e:
        logger.error(f"Error in train_model route: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        file_path = save_uploaded_file(file)
        content = get_file_content(file_path)
        processed_data = preprocess_data(pd.read_csv(file_path))
        return jsonify({
            'message': 'File uploaded successfully',
            'content': content,
            'processed_data': processed_data.to_dict()
        })

@app.route('/start_streaming', methods=['POST'])
def start_data_streaming():
    symbols = request.json.get('symbols', ['BTCUSDT', 'ETHUSDT'])
    try:
        start_streaming(symbols)
        return jsonify({'message': 'Streaming started successfully'}), 200
    except Exception as e:
        logger.error(f"Error in start_data_streaming route: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/backtest', methods=['POST'])
def run_backtest():
    symbol = request.json.get('symbol', 'BTCUSDT')
    start_date = request.json.get('start_date', '2022-01-01')
    end_date = request.json.get('end_date', '2023-05-01')
    initial_capital = request.json.get('initial_capital', 100000)
    
    results = backtest(symbol, start_date, end_date, initial_capital)
    return jsonify(results)

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
    return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=True)