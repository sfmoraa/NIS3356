from PreProgress.utils import process_csv
from plots.plot import plot
filename = "CrawlingStuff/CrawlResult/#除夕不放假#.csv"
data = process_csv(filename)
print(data)
myplot = plot(data)
myplot.Review_amount(step="hour",minlength = 0,start_date = "2023-01-01",end_date = "2023-10-27") 
