# NIS3356
A course design on information content security, intended to crawl and analyze specified topics on social networks.

## 文件目录说明
- `analysis`: 数据分析，包括性别比例，时间趋势分析，地域分析
- `cluster`: 聚类分析，主要是Kmeans聚类
- `CrawlingStuff`: 网络爬虫
- `model`: 中文文本处理模型，包括 `Bert`、 `TFIDF` 、`Word2Vec`.
- `output`: 输出结果
- `plot`: 作图函数以及作图结果
- `bert.py`: 利用Bert模型进行处理文件的样例
- `LDA.py`: 利用LDA模型进行处理文件的样例
- `word2vec.py`: 利用Word2Vec模型进行处理文件的样例

## CrawlingStuff说明
运行main_crawl.py，可自由设定要搜索的内容/话题，结果存储路径，搜索日期范围。

爬取对象为指定日期范围内微博高级搜索的逐日搜索结果，每条数据含评论文字内容及相对于爬取时间点的评论发布时间。