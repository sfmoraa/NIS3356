import numpy as np
import torch 
from PreProgress.utils import process_csv
from transformers import BertTokenizer, BertModel

# https://huggingface.co/bert-base-chinese/tree/main
BRET_PATH = "PreProgress/Bert/bert-base-chinese"


def bert_process(filename: str, max_length: int=50, device: str="cpu"):
    assert filename.endswith('.csv'), f'filename is invalid!'
    # use tokenizer to get encoding the text
    data = process_csv(filename)
    text = data['text'].tolist()
    tokenizer = BertTokenizer.from_pretrained(BRET_PATH)
    tokens = tokenizer(text, padding='max_length', max_length = max_length, truncation =True)
    input_ids = torch.tensor(tokens["input_ids"]).to(device)
    attn_mask = torch.tensor(tokens["attention_mask"]).to(device)
    # use model to get the features
    model = BertModel.from_pretrained(BRET_PATH).to(device)
    outputs = model(input_ids, attention_mask=attn_mask)
    features = outputs.last_hidden_state
    return features