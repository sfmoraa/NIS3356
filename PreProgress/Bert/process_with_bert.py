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
    last_hidden_states = []
    pooler_outputs = []
    with torch.no_grad():
        for batch in dataloader:
            batch_input_ids, batch_attention_mask = batch
            batch_input_ids = batch_input_ids.to(device)
            batch_attention_mask = batch_attention_mask.to(device)
            # Get features from BERT model
            outputs = model(batch_input_ids, attention_mask=batch_attention_mask)
            last_hidden_state = outputs.last_hidden_state
            pooler_output = outputs.pooler_output
            last_hidden_states.append(last_hidden_state)
            pooler_outputs.append(pooler_output)

    # Concatenate features from all batches
    last_hidden_states = torch.cat(last_hidden_states, dim=0)
    last_hidden_states = last_hidden_states.detach().cpu().numpy()
    pooler_outputs = torch.cat(pooler_outputs, dim=0)
    pooler_outputs = pooler_outputs.detach().cpu().numpy()
    return last_hidden_states, pooler_outputs