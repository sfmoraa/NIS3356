import numpy as np
import pandas as pd
import utils
import os
data = pd.read_csv("../CrawlingStuff/CrawlResult/#除夕不放假#.csv",names=["text","times"])
data = data[1:]
data = data.dropna()
raw_data = utils.preprocess_with_bert(data,maxlength = 50)
print(raw_data)
print(raw_data.shape)