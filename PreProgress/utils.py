import pandas as pd
import os
import re
import jieba

def process_csv(filename: str, with_labels = False):
    assert filename.endswith('.csv'), f'filename is invalid!'
    if with_labels == True:
        ori_data = pd.read_csv(filename)
    else:
        ori_data = pd.read_csv(filename, names=['text','time'])[1:]
    data = ori_data.dropna()
    data = data[~data['text'].str.startswith('【')]
    return data

def divide_csv(filename,labels,model_name):
    data = process_csv(filename)
    data['labels'] = labels
    data_1 = data[data["labels"] == 1]
    data_2 = data[data["labels"] == 0]
    hash_index = filename.find("#")
    if hash_index != -1 and len(filename) >= hash_index + 4:
        to_filename = filename[hash_index + 1:hash_index + 4]
    else :
        return
    folder_path = "divided_data/" + to_filename
    os.makedirs(folder_path, exist_ok=True)
    data_1.to_csv("divided_data/" + to_filename +"/"+ model_name +"1.csv",encoding="utf_8_sig")
    data_2.to_csv("divided_data/" + to_filename +"/"+ model_name + "2.csv",encoding="utf_8_sig")
    return 


def clean_text(text):
    """
    Remove special characters, punctuation marks, excess spaces
    """
    text = re.sub("[^\u4e00-\u9fa5a-zA-Z0-9]", "", text)
    text = re.sub("\s+", " ", text)
    text = text.lower()
    return text


def tokenize(text):
    """
    Using jieba for word segmentation
    """
    words = jieba.lcut(text)
    return words


def remove_stopwords(tokens):
    """
    Remove some stop words
    """
    stopwords = set(['的', '了', '是', '在', '我', '有', '和', '就', '不', '人','你','吧','啊'])
    filtered_tokens = [token for token in tokens if token not in stopwords]
    return filtered_tokens

def getstr(tokens):
    """
    Remove some stop words
    """
    result_str = ' '.join(tokens)
    return result_str