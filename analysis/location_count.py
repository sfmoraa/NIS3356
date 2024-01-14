import pandas as pd
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


plt.rcParams['font.family'] = 'Microsoft YaHei'


config = {
    'file_path': "../CrawlingStuff/CrawlResult/WEIBO_#张雪峰回应文科都是服务业#.csv",
    'location_column_number': 3,
}


def analyze_location_ratio(file_path=None, location_column_number=None):
    df = pd.read_csv(file_path)
    location_counts = df.iloc[:, location_column_number].value_counts().to_dict()

    plt.bar(location_counts.keys(), location_counts.values())
    plt.xlabel('Keys')
    plt.ylabel('Values')
    plt.title('Bar Chart')
    plt.show()


analyze_location_ratio(**config)
