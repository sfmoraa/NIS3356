import re
import jieba
import numpy as np
from gensim.models import Word2Vec
from PreProgress.utils import process_csv


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
    stopwords = set(['的', '了', '是', '在', '我', '有', '和', '就', '不', '人'])
    filtered_tokens = [token for token in tokens if token not in stopwords]
    return filtered_tokens


def word2vec_process(filename: str):
    """
    Using word2vec method to obtain word vectors
    """
    assert filename.endswith('.csv'), f'filename is invalid!'
    
    # preprocess for the data of the target file
    data = process_csv(filename)
    data['text'] = data['text'].apply(clean_text)
    data['tokens'] = data['text'].apply(tokenize)
    data['tokens'] = data['tokens'].apply(remove_stopwords)
    
    # Initial the Model
    model = Word2Vec(data['tokens'], vector_size=100, window=5, min_count=1, workers=4)
    
    # Convert text to vectors
    vectors = []
    for tokens in data['tokens']:
        token_vectors = [model.wv[token] for token in tokens if token in model.wv]
        if token_vectors:
            avg_vector = np.mean(token_vectors, axis=0)
            vectors.append(avg_vector)
        else:
            # if the tag is not in the vocabulary, use zero vector padding
            vectors.append(np.zeros(100))  
    vectors = np.array(vectors)
    return vectors
