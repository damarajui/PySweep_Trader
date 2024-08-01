from models.trading_algorithm import TradingAlgorithm
from utils.data_collection import collect_data
from utils.data_preprocessing import preprocess_data


class FileProcessor:
    def __init__(self):
        self.trading_algo = TradingAlgorithm()

    def process_file(self, file_path: str):
        raw_data = collect_data(file_path)
        processed_data = preprocess_data(raw_data)
        predictions = self.trading_algo.predict(processed_data)
        return predictions