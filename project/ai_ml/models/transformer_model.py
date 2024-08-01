from typing import Dict, List

import torch
import torch.nn as nn
from transformers import BertModel, Trainer, TrainingArguments


class TransformerTimeSeriesModel(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(TransformerTimeSeriesModel, self).__init__()
        self.bert = BertModel.from_pretrained('bert-base-uncased')
        self.fc = nn.Linear(self.bert.config.hidden_size, output_dim)
    
    def forward(self, x):
        outputs = self.bert(x)
        logits = self.fc(outputs.last_hidden_state)
        return logits

def prepare_data(data: Dict[str, List[float]]) -> torch.Tensor:
    # Convert dictionary to tensor
    # This is a placeholder and should be implemented based on your specific data structure
    return torch.tensor([list(data.values())], dtype=torch.float32)

def train_model(train_dataset, eval_dataset, num_epochs=3, learning_rate=2e-5, batch_size=32):
    model = TransformerTimeSeriesModel(input_dim=128, output_dim=1)
    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=num_epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir='./logs',
        logging_steps=10,
        learning_rate=learning_rate,
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset
    )
    
    try:
        trainer.train()
        trainer.save_model("./saved_model")
        return model
    except Exception as e:
        print(f"An error occurred during training: {e}")
        return None

def predict(model: TransformerTimeSeriesModel, data: Dict[str, List[float]]) -> float:
    model.eval()
    with torch.no_grad():
        input_tensor = prepare_data(data)
        output = model(input_tensor)
        return output.item()

def load_model(model_path: str) -> TransformerTimeSeriesModel:
    model = TransformerTimeSeriesModel(input_dim=128, output_dim=1)
    model.load_state_dict(torch.load(model_path))
    return model