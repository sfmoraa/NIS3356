from PreProgress import word2vec_process
from Cluster import kmeans


filename = "CrawlingStuff/CrawlResult/#除夕不放假#.csv"
word_outputs = word2vec_process(filename)
lables = kmeans(word_outputs)
print(lables)