from transformers import AutoTokenizer,  AutoModelForMaskedLM
import torch
import numpy as np
def preprocess_with_bert(data,maxlength = 50):
    X = data['text'].tolist()
    tokenizer = AutoTokenizer.from_pretrained("models/bert-base-chinese/")
    if maxlength:
        tokens = tokenizer(X, padding='max_length',max_length = maxlength, truncation =True)
    else:
        tokens = tokenizer(X, padding=True, truncation =True)
    return np.array(tokens["input_ids"])
    