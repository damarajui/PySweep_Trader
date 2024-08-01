import pandas as pd
import torch
from ai_ml.models.transformer_model import (
    TransformerTimeSeriesModel,
    predict,
    prepare_data,
)


class TradingAlgorithm:
    def __init__(self):
        self.model = TransformerTimeSeriesModel(input_dim=128, output_dim=1)
        self.model.load_state_dict(torch.load("./saved_model/pytorch_model.bin"))
        self.model.eval()

    def predict(self, data):
        if isinstance(data, pd.DataFrame):
            predictions = []
            for _, row in data.iterrows():
                processed_data = prepare_data(row.to_dict())
                prediction = predict(self.model, processed_data)
                predictions.append(self.get_decision(prediction))
            return predictions
        else:
            processed_data = prepare_data(data)
            prediction = predict(self.model, processed_data)
            return self.get_decision(prediction)

    def get_decision(self, prediction):
        if prediction > 0.7:
            return "STRONG_BUY"
        elif prediction > 0.3:
            return "BUY"
        elif prediction < -0.7:
            return "STRONG_SELL"
        elif prediction < -0.3:
            return "SELL"
        else:
            return "HOLD"

class MovingAverageCrossover:
    def __init__(self, short_window=20, long_window=50):
        self.short_window = short_window
        self.long_window = long_window

    def predict(self, data):
        if len(data) < self.long_window:
            return "HOLD"
        
        short_ma = data['close'].rolling(window=self.short_window).mean().iloc[-1]
        long_ma = data['close'].rolling(window=self.long_window).mean().iloc[-1]
        
        if short_ma > long_ma:
            return "BUY"
        elif short_ma < long_ma:
            return "SELL"
        else:
            return "HOLD"