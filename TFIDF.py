from PreProgress import TFIDF_process
from Cluster import kmeans


filename = "CrawlingStuff\CrawlResult\WEIBO_#张雪峰回应文科都是服务业#.csv"
word_outputs = TFIDF_process(filename)
lables = kmeans(word_outputs)
print(lables.sum())