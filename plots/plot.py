from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
def process_time(time_str):
    # 将时间字符串解析为datetime对象
    current_year = datetime.now().year
    datetime_str = f"{current_year}年" + time_str
    datetime_obj = datetime.strptime(datetime_str, "%Y年%m月%d日 %H:%M")
    
    # 提取日期、小时和分钟
    year = datetime_obj.year
    month = datetime_obj.month
    day = datetime_obj.day
    hour = datetime_obj.hour
    minute = datetime_obj.minute
    
    return year, month,day, hour, minute
class plot():  ## 传入一个dataframe
    def __init__(self,textdata):
        self.data = textdata
        self.data[["year", "month","day", "hour", "minute"]] = self.data["time"].apply(lambda x: pd.Series(process_time(x)))
        print(self.data)
    def Review_amount(self,step = "day",minlength = 0,start_date = "2023-01-01",end_date = "2023-12-31"):   ## 评论数量变化
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
        
    # def Review_amount(self,step = "day",minlength = 0,start_date = "2023-01-01",end_date = "2023-12-31"):   ## 评论数量变化
    #     start_date = pd.to_datetime(start_date)
    #     end_date = pd.to_datetime(end_date)
    #     legends = ['topic1']
    #     if step == "day":
    #         review_num_to_hour = self.data.groupby(['year','month','day'])['text'].count()
    #     elif step == "hour":
    #         review_num_to_hour = self.data.groupby(['year','month','day','hour'])['text'].count()
        
    #     review_num_to_hour.columns = legends
    #     review_num_to_hour = review_num_to_hour.reset_index()
    #     review_num_to_hour = review_num_to_hour[review_num_to_hour["text"] >= minlength]
    #     if step == "day":
    #         review_num_to_hour['date'] = pd.to_datetime(review_num_to_hour[["year","month","day"]])
    #         review_num_to_hour = review_num_to_hour.drop(['year','month','day'], axis=1).set_index('date')
    #     elif step == 'hour' :
    #         review_num_to_hour['date'] = pd.to_datetime(review_num_to_hour[["year","month","day","hour"]])
    #         review_num_to_hour = review_num_to_hour.drop(['year','month','day',"hour"], axis=1).set_index('date')
    #     review_num_to_hour = review_num_to_hour.loc[(review_num_to_hour.index >= start_date) & (review_num_to_hour.index <= end_date)]
    #     review_num_to_hour.plot(legend=True, alpha=0.5)
    #     plt.xlabel('Date')
    #     plt.ylabel('Amount')
    #     plt.savefig("plots/figures/Review Amount per day.png", dpi=500, bbox_inches = 'tight')
    #     plt.show()






