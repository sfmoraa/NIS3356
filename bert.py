from PreProgress import bert_process


filename = "CrawlingStuff/CrawlResult/#除夕不放假#.csv"
aa = bert_process(filename, device="cuda")
print(aa)