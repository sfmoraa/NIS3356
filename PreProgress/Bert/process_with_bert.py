import numpy as np
import torch 
from torch.utils.data import TensorDataset
from PreProgress.utils import process_csv
from transformers import BertTokenizer, BertModel
from torch.utils.data import DataLoader

# https://huggingface.co/bert-base-chinese/tree/main
BERT_PATH = "PreProgress/Bert/bert-base-chinese"


def bert_process(filename: str, batch_size: int = 32, max_length: int = 50, device: str = "cpu"):
    assert filename.endswith('.csv'), 'Invalid filename!'

    # Load data from CSV file
    data = process_csv(filename)
    text = data['text'].tolist()

    # Initialize tokenizer and model
    tokenizer = BertTokenizer.from_pretrained(BERT_PATH)
    model = BertModel.from_pretrained(BERT_PATH).to(device)

    # Tokenize and encode the text
    encoded_inputs = tokenizer(text, padding='max_length', max_length=max_length, truncation=True)
    input_ids = torch.tensor(encoded_inputs["input_ids"]).to(device)
    attention_mask = torch.tensor(encoded_inputs["attention_mask"]).to(device)

    # Create DataLoader for batch processing
    dataset = TensorDataset(input_ids, attention_mask)
    dataloader = DataLoader(dataset, batch_size=batch_size)

    # Process the text in batches
    all_features = []
    with torch.no_grad():
        for batch in dataloader:
            batch_input_ids, batch_attention_mask = batch
            batch_input_ids = batch_input_ids.to(device)
            batch_attention_mask = batch_attention_mask.to(device)

            # Get features from BERT model
            outputs = model(batch_input_ids, attention_mask=batch_attention_mask)
            features = outputs.last_hidden_state

            all_features.append(features)

    # Concatenate features from all batches
    features = torch.cat(all_features, dim=0)

    return features