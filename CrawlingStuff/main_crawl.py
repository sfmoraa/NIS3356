from data_crawling import weibo_crawl_topic, zhihu_crawl_topic


# weibo_topic = "#张雪峰回应文科都是服务业#"
# weibo_result_file_path = "./CrawlResult/WEIBO_" + weibo_topic + ".csv"
# search_days_range = ["2023-12-05-0", "2023-12-22-18"]
# weibo_crawl_topic(weibo_topic, weibo_result_file_path, search_days_range)

zhihu_question_dic={"除夕不放假":627703982,"五月天巴黎演唱会解读":633863052,"王自如言论":630284414,'如何评价张雪峰称文科都是服务业？':634052854}
zhihu_topic="如何评价张雪峰称文科都是服务业？"
zhihu_question_number=zhihu_question_dic[zhihu_topic]
zhihu_result_file_path= "./CrawlResult/ZHIHU_" + zhihu_topic + ".csv"
zhihu_crawl_topic(zhihu_question_number,zhihu_result_file_path)
