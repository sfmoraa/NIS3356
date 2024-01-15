from model import TFIDF_process
from Cluster import kmeans
from model.utils import divide_csv
import matplotlib.pyplot as plt
from sklearn.cluster import MiniBatchKMeans
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE


def plot_tsne_scatter(data, labels, n_components=2):
    embedded_data = data
    tsne = TSNE(n_components=n_components, random_state=42)
    embedded_data = tsne.fit_transform(data)
    
        # 绘制散点图
    plt.figure(figsize=(8, 8))
    unique_labels = np.unique(labels)
    colors = ['lightpink','deepskyblue']
    for i, label in enumerate(unique_labels):
        mask = labels == label
        plt.scatter(embedded_data[mask, 0], embedded_data[mask, 1], c=colors[i], label=label,s=7)
    
    # 设置图例和标题
    plt.legend()
    plt.title('t-SNE Scatter Plot')
    
    # 显示图形
    plt.show()
    
data = pd.read_csv("raw_data_clustered_weibo.csv",encoding = 'utf-8-sig')
text = data["embedding"].tolist()
text = np.array([list(map(float, item.strip('[]').split()))for item in text])
labels = data["Kmeans_2"]

plot_tsne_scatter(text, labels)