from PreProgress.utils import process_csv
from plots.plot import plot
filename = "CrawlingStuff\CrawlResult\WEIBO_#张雪峰回应文科都是服务业#.csv"
data = process_csv(filename)
myplot = plot(data)
myplot.Review_amount(step="hour",minlength = 0,start_date = "2023-12-09",end_date = "2023-12-10") 
