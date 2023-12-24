import pandas as pd
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

config = {
    'file_path': "../CrawlingStuff/CrawlResult/WEIBO_#张雪峰回应文科都是服务业#.csv",
    'gender_column_number': 4,
    'male_symbol': 'm',
    'female_symbol': 'f',
    'unknown_symbol': '-1',
}


def analyze_gender_ratio(file_path=None, gender_column_number=None, male_symbol=None, female_symbol=None, unknown_symbol=None):
    df = pd.read_csv(file_path)
    gender_counts = df.iloc[:, gender_column_number].value_counts().to_dict()
    gender= {}
    if male_symbol in gender_counts:
        gender["Male"]=gender_counts[male_symbol]
    if female_symbol in gender_counts:
        gender["Female"]=gender_counts[female_symbol]
    if unknown_symbol in gender_counts:
        gender["Unknown"]=gender_counts[unknown_symbol]
    print(gender)

    plt.pie(gender.values(), labels=gender.keys(), autopct='%1.1f%%')
    plt.axis('equal')
    plt.title('Gender Distribution')
    plt.show()


analyze_gender_ratio(**config)
