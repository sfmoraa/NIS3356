import pandas as pd


def merge_to_csv(data_list, output_path,topic,query_time):
    df = pd.DataFrame(data_list, columns=[topic, query_time])
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
