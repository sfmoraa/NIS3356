import numpy as np
from sklearn.cluster import KMeans


def kmeans(features: np.ndarray, num_clusters: int=2):
    kmeans = KMeans(n_clusters=num_clusters)
    cluster_labels = kmeans.fit_predict(features)
    return cluster_labels