import os
import torch
from backend.utils.data_collection import collect_data
from backend.utils.data_preprocessing import preprocess_data
from models.transformer_model import TransformerTimeSeriesModel, train_model
from sklearn.model_selection import train_test_split

def prepare_dataset(data):
    X = data[['open', 'high', 'low', 'close', 'volume', 'return', 'log_return', 'volatility', 'sma_20', 'sma_50', 'rsi']]
    y = data['close'].shift(-1)  # Predict next day's closing price
    X = X[:-1]  # Remove last row
    y = y[:-1]  # Remove last row
    return X, y

def main(symbol='AAPL', start_date='2010-01-01', end_date='2023-05-01', model_version='v1'):
    # Collect and preprocess data
    raw_data = collect_data(symbol, start_date, end_date)
    processed_data = preprocess_data(raw_data)
    
    # Prepare dataset
    X, y = prepare_dataset(processed_data)
    
    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the model
    model = train_model(X_train, y_train, X_test, y_test)
    
    # Save the trained model
    save_path = f"./saved_models/{model_version}"
    os.makedirs(save_path, exist_ok=True)
    torch.save(model.state_dict(), f"{save_path}/pytorch_model.bin")
    
    print(f"Model saved as version: {model_version}")

if __name__ == "__main__":
    main()