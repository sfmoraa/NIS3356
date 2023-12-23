from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import jieba
import matplotlib.pyplot as plt
from PreProgress.utils import process_csv
import re
from PreProgress.utils import *




def TFIDF_process(filename: str, with_labels = False):
    """
    Using word2vec method to obtain word vectors
    """
    assert filename.endswith('.csv'), f'filename is invalid!'
    
    # preprocess for the data of the target file
    data = process_csv(filename,with_labels)
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
    return tfidf_weight,decomposition_data, word
    