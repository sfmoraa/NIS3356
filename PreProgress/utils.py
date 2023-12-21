import pandas as pd


def process_csv(filename: str):
    assert filename.endswith('.csv'), f'filename is invalid!'
    ori_data = pd.read_csv(filename, names=['text', 'time'])[1:]
    data = ori_data.dropna()
    return data
