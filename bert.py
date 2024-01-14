from Models import bert_process
from Cluster import kmeans
from Models.utils import divide_csv

filename = "CrawlingStuff\CrawlResult\WEIBO_#张雪峰回应文科都是服务业#.csv"
last_hidden_states, pooler_outputs = bert_process(filename, device="cuda")
print(pooler_outputs.shape)
lables = kmeans(pooler_outputs)
print(lables)

divide_csv(filename,lables,model_name = "bert")