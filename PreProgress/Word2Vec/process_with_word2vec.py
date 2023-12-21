import numpy as np
import pandas as pd
from gensim.models import Word2Vec
data = pd.read_csv("../CrawlingStuff/CrawlResult/#除夕不放假#.csv",names=["text","times"])
data = data[1:]
data = data.dropna()
import jieba
import re
def clean_text(text):
    # 去除特殊字符和标点符号
    text = re.sub("[^\u4e00-\u9fa5a-zA-Z0-9]", "", text)
    # 去除多余的空格
    text = re.sub("\s+", " ", text)
    # 转换为小写
    text = text.lower()
    return text

data['text'] = data['text'].apply(clean_text)
def tokenize(text):
    # 使用jieba进行分词
    words = jieba.lcut(text)
    return words

data['tokens'] = data['text'].apply(tokenize)
def remove_stopwords(tokens):
    stopwords = set(['的', '了', '是', '在', '我', '有', '和', '就', '不', '人'])
    filtered_tokens = [token for token in tokens if token not in stopwords]
    return filtered_tokens

data['tokens'] = data['tokens'].apply(remove_stopwords)

model = Word2Vec(data['tokens'], vector_size=100, window=5, min_count=1, workers=4)

# 将文本标记转换为向量
vectors = []
for tokens in data['tokens']:
    token_vectors = [model.wv[token] for token in tokens if token in model.wv]
    if token_vectors:
        avg_vector = np.mean(token_vectors, axis=0)
        vectors.append(avg_vector)
    else:
        vectors.append(np.zeros(100))  # 如果标记未在词汇表中，则使用零向量填充

vectors = np.array(vectors)
print(vectors)
print(vectors.shape)
