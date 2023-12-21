import pandas as pd
import os

def process_csv(filename: str):
    assert filename.endswith('.csv'), f'filename is invalid!'
    ori_data = pd.read_csv(filename, names=['text','time'])[1:]
    data = ori_data.dropna()
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