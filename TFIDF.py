from model import TFIDF_process
from cluster import kmeans
from model.utils import divide_csv

filename = "CrawlingStuff/CrawlResult/WEIBO_#张雪峰回应文科都是服务业#.csv"
word_outputs,_,_ = TFIDF_process(filename)
lables = kmeans(word_outputs)
print(lables.sum())
divide_csv(filename, lables, model_name = "TFIDF")