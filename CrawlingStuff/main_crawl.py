from data_crawling import crawl_topic


topic="#除夕不放假#"
result_file_path="./CrawlResult/"+topic+".csv"
search_days_range=["2023-10-22-0","2023-12-17-23"]

crawl_topic(topic,result_file_path,search_days_range)



