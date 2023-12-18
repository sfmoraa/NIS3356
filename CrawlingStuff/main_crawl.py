from data_crawling import weibo_crawl_topic,zhihu_crawl_topic

def
# weibo_topic= "#除夕不放假#"
# weibo_result_file_path= "./CrawlResult/WEIBO_" + weibo_topic + ".csv"
# search_days_range=["2023-10-22-0","2023-12-17-23"]
# weibo_crawl_topic(weibo_topic, weibo_result_file_path, search_days_range)


zhihu_question_dic={"除夕不放假":627703982,"五月天巴黎演唱会解读":633863052,"王自如言论":630284414}
zhihu_topic="王自如言论"
zhihu_question_number=zhihu_question_dic[zhihu_topic]
zhihu_result_file_path= "./CrawlResult/ZHIHU_" + zhihu_topic + ".csv"
zhihu_crawl_topic(zhihu_question_number,zhihu_result_file_path)



