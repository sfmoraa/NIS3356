from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from Models.utils import getstr, clean_text, tokenize, remove_stopwords
from collections import Counter
import wordcloud
import seaborn as sns


def process_time(time_str: str):
    """
    Retrieve time information from a time string
    """
    # Parse the time string into a datatime object
    datetime_obj = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
    year = datetime_obj.year
    month = datetime_obj.month
    day = datetime_obj.day
    hour = datetime_obj.hour
    minute = datetime_obj.minute
    return year, month, day, hour, minute


class plot():
    def __init__(self, textdata: pd.DataFrame):
        self.data = textdata
        self.data[["year", "month","day", "hour", "minute"]] = \
            self.data["time"].apply(lambda x: pd.Series(process_time(x)))
        self.data['processed_text'] = self.data['text'].apply(clean_text)
        self.data['tokens'] = self.data['processed_text'].apply(tokenize)
        self.data['tokens'] = self.data['tokens'].apply(remove_stopwords)
    
    def review_amount(
        self, 
        step: str="day",
        minlength: int=0,
        start_date: str="2023-01-01",
        end_date: str="2023-12-31"
    ):
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        legends = ['topic1']
        if step == "day":
            review_num_to_hour = self.data.groupby(['year','month','day'])['text'].count()
        elif step == "hour":
            review_num_to_hour = self.data.groupby(['year','month','day','hour'])['text'].count()
        
        review_num_to_hour.columns = legends
        review_num_to_hour = review_num_to_hour.reset_index()
        review_num_to_hour = review_num_to_hour[review_num_to_hour["text"] >= minlength]
        if step == "day":
            review_num_to_hour['date'] = pd.to_datetime(review_num_to_hour[["year","month","day"]])
            review_num_to_hour = review_num_to_hour.drop(['year','month','day'], axis=1).set_index('date')
        elif step == 'hour' :
            review_num_to_hour['date'] = pd.to_datetime(review_num_to_hour[["year","month","day","hour"]])
            review_num_to_hour = review_num_to_hour.drop(['year','month','day',"hour"], axis=1).set_index('date')
        review_num_to_hour = review_num_to_hour.loc[(review_num_to_hour.index >= start_date) & (review_num_to_hour.index <= end_date)]
        review_num_to_hour.plot(legend=True, alpha=0.5)
        plt.xlabel('Date')
        plt.ylabel('Amount')
        # plt.savefig("plots/figures/Review Amount per day.png", dpi=500, bbox_inches = 'tight')
        plt.show()

    def word_frequency(self):
        tokens_list = self.data["tokens"].tolist()
        tokens_list = [i for ii in tokens_list for i in ii]
        word_count = Counter(tokens_list)
        top_words = sorted(word_count.items(),key = lambda x : x[1], reverse=True)[:10]
        print(top_words)

    def word_cloud(self, savefile,stopwords):
        tokens_list = self.data["tokens"].tolist()
        tokens_list = [i for ii in tokens_list for i in ii]
        tokens_list = getstr(tokens_list)
        wc = wordcloud.WordCloud(font_path="msyh.ttc",
                         width = 1000,
                         height = 700,
                         background_color='white',
                         max_words=30,stopwords=stopwords)
        wc.generate(tokens_list)
        wc.to_file("plots/figures/" +savefile)
    
    def review_length(self,start_date = "2023-01-01",end_date = "2023-12-31"):   ## 评论长度分布
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        review_length= self.data
        review_length["lens"] = review_length["text"].apply(lambda x : len(x))
        review_length['date'] = pd.to_datetime(review_length[["year","month","day","hour"]])
        review_length = review_length.loc[(review_length["date"] >= start_date) & (review_length["date"] <= end_date)]
        sns.histplot(review_length["lens"])
        plt.xlabel('len')
        plt.ylabel('Frequency')
        plt.title('Histogram')
        # plt.savefig("plots/figures/Review Amount per day.png", dpi=500, bbox_inches = 'tight')
        plt.show()




