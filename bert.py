from PreProgress import bert_process
from Cluster import kmeans

filename = "CrawlingStuff/CrawlResult/#除夕不放假#.csv"
last_hidden_states, pooler_outputs = bert_process(filename, device="cuda")
lables = kmeans(pooler_outputs)
print(lables)