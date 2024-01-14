from model import word2vec_process
from cluster import kmeans
from model.utils import divide_csv

filename = "CrawlingStuff\CrawlResult\WEIBO_#张雪峰回应文科都是服务业#.csv"
word_outputs = word2vec_process(filename)
lables = kmeans(word_outputs)
print(lables)

divide_csv(filename, lables, model_name="word2vec")