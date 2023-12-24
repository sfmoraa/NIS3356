from PreProgress.utils import process_csv
from PreProgress import TFIDF_process
from plots.plot import plot
def plot_for_view_numbers():
    filename = "CrawlingStuff\CrawlResult\WEIBO_#张雪峰回应文科都是服务业#.csv"
    data = process_csv(filename)
    myplot = plot(data)
    myplot.Review_amount(step="hour",minlength = 0,start_date = "2023-12-09",end_date = "2023-12-10") 

def plot_for_word_cloud():
    filename = "divided_data/张雪峰/bert1.csv"
    data =  process_csv(filename,with_labels=True)
    myplot = plot(data)
    stopwords = ["的","是","了","张","雪峰","文科","服务业","服务","什么","觉得","这有","所谓","都","也","舔"]
    myplot.word_cloud(stopwords=stopwords, savefile = "张雪峰bert1词云.png")

def plot_for_word_frequency():
    filename = "divided_data/张雪峰/bert1.csv"
    data =  process_csv(filename,with_labels=True)
    myplot = plot(data)
    myplot.Review_length(start_date = "2023-12-09",end_date = "2023-12-31")

# plot_for_view_numbers()  
plot_for_word_cloud()
# plot_for_word_frequency()

