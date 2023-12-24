import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def extract_hourly_data(file_path, time_column):
    df = pd.read_csv(file_path)
    df.iloc[:, time_column] = pd.to_datetime(df.iloc[:, time_column])
    df.set_index(df.columns[time_column], inplace=True)
    hourly_counts = df.resample('H').size()
    return hourly_counts


def plot_in_one(alllist):
    fig, ax = plt.subplots()
    for i in range(len(alllist)):
        ax.plot(alllist[i].index, alllist[i].values, label='type' + str(i + 1))

    ax.legend()
    ax.set_xlabel('time')
    ax.set_ylabel('count')

    plt.show()


if __name__ == '__main__':
    type1 = extract_hourly_data("../divided_data/张雪峰/bert1.csv", 2)
    type2 = extract_hourly_data("../divided_data/张雪峰/bert2.csv", 2)
    plot_in_one([type1, type2])
    type1 = extract_hourly_data("../divided_data/张雪峰/TFIDF1.csv", 2)
    type2 = extract_hourly_data("../divided_data/张雪峰/TFIDF2.csv", 2)
    plot_in_one([type1, type2])
    type1 = extract_hourly_data("../divided_data/张雪峰/word2vec1.csv", 2)
    type2 = extract_hourly_data("../divided_data/张雪峰/word2vec2.csv", 2)
    plot_in_one([type1, type2])