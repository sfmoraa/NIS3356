from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import jieba
import matplotlib.pyplot as plt
from PreProgress.utils import process_csv
import re

def clean_text(text):
    """
    Remove special characters, punctuation marks, excess spaces
    """
    text = re.sub("[^\u4e00-\u9fa5a-zA-Z0-9]", "", text)
    text = re.sub("\s+", " ", text)
    text = text.lower()
    return text


def tokenize(text):
    """
    Using jieba for word segmentation
    """
    words = jieba.lcut(text)
    return words


def remove_stopwords(tokens):
    """
    Remove some stop words
    """
    stopwords = set(['的', '了', '是', '在', '我', '有', '和', '就', '不', '人','你'])
    filtered_tokens = [token for token in tokens if token not in stopwords]
    return filtered_tokens

def getstr(tokens):
    """
    Remove some stop words
    """
    result_str = ' '.join(tokens)
    return result_str


def TFIDF_process(filename: str):
    """
    Using word2vec method to obtain word vectors
    """
    assert filename.endswith('.csv'), f'filename is invalid!'
    
    # preprocess for the data of the target file
    data = process_csv(filename)
    data['text'] = data['text'].apply(clean_text)
    data['tokens'] = data['text'].apply(tokenize)
    data['tokens'] = data['tokens'].apply(remove_stopwords)
    data['tokens'] = data['tokens'].apply(getstr)
    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(vectorizer.fit_transform(data['tokens']))
    word = vectorizer.get_feature_names()      
    print("word feature length: {}".format(len(word)))
    tfidf_weight = tfidf.toarray() ## 权重

    tsne = TSNE(n_components=2)
    decomposition_data = tsne.fit_transform(tfidf_weight)   ## T-SNE降维
    print(tfidf_weight.shape)
    print(decomposition_data.shape)
    return tfidf_weight
    