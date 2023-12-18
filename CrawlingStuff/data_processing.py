import pandas as pd


def weibo_store_data(data_list, output_path, topic, query_time):
    df = pd.DataFrame(data_list, columns=[topic, query_time])
    df.to_csv(output_path, index=False, encoding='utf-8-sig')

def zhihu_store_data(data_list, output_path, topic):
    df = pd.DataFrame(data_list, columns=[topic, "gender","comments","likes","updated_time"])
    df.to_csv(output_path, index=False, encoding='utf-8-sig')