from model import bert_process
from Cluster import kmeans
from model.utils import *
from transformers import BertTokenizer, BertModel
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import torch
from torch.utils.data import DataLoader
from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn import metrics
from tqdm import tqdm
from sklearn.manifold import TSNE

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')  # 设备
def plot_tsne_scatter(data, labels, n_components=2):

    tsne = TSNE(n_components=n_components, random_state=42)
    embedded_data = tsne.fit_transform(data)
    
        # 绘制散点图
    plt.figure(figsize=(8, 8))
    unique_labels = np.unique(labels)
    colors = plt.cm.rainbow(np.linspace(0, 1, len(unique_labels)))
    for i, label in enumerate(unique_labels):
        mask = labels == label
        plt.scatter(embedded_data[mask, 0], embedded_data[mask, 1], c=colors[i], label=label)
    
    # 设置图例和标题
    plt.legend()
    plt.title('t-SNE Scatter Plot')
    
    # 显示图形
    plt.show()
def encoding(model, tokenizer, sentences):
    model.eval()
    model.to(device)
    max_char_len = 128
    sents_inputs = tokenizer(sentences, return_tensors='pt', max_length=max_char_len, padding="max_length", truncation=True)
    input_ids = sents_inputs['input_ids']
    dataloader = DataLoader(input_ids, batch_size=2, shuffle=False)
    sents_vec = []
    tqdm_batch_iterator = tqdm(dataloader, desc='sentence encoding ')
    for index, batch in enumerate(tqdm_batch_iterator):
        input_ids = batch
        input_ids = input_ids.to(device)
        sents_vec.append(model(input_ids)['pooler_output'].detach().cpu().numpy().tolist())
    torch.cuda.empty_cache()
    sents_vec = [np.array(xi) for x in sents_vec for xi in x]
    return sents_vec
def K_cluster_analysis(K, X):
    print("K-means begin with clusters: {}".format(K))
    # K-means,在训练集上训练,病返回聚类silhouette_score等得分，分数越大越好
    mb_kmeans = MiniBatchKMeans(n_clusters=K, init="k-means++") # KMeans在大数据量时速度较慢
    y_pred = mb_kmeans.fit_predict(X)
    CH_score = metrics.calinski_harabasz_score(X, y_pred)
    si_score = metrics.silhouette_score(X, y_pred)
    print("CH_score: {}".format(CH_score))
    print("si_score: {}".format(si_score))
    return CH_score, si_score

if __name__ == "__main__":
    filename = "CrawlingStuff\CrawlResult\小红书评论_张雪峰文科就是服务业.csv"
    data = process_csv(filename,with_labels=True).reset_index()
    BERT_PATH = "PreProgress/Bert/bert-base-chinese"
    tokenizer = BertTokenizer.from_pretrained(BERT_PATH)
    model = BertModel.from_pretrained(BERT_PATH).to(device)
    # sentence_list = data["sentence"].tolist()
    # last_hidden_states, sents_vec = bert_process(filename, device="cuda",with_labels=True)
    # data = process_csv(filename,with_labels = True)
    sentence_list = data["text"].tolist()
    sents_vec = encoding(model, tokenizer, sentence_list)
    tsne = TSNE(n_components=2)
    sents_vec = tsne.fit_transform(sents_vec)
    sents_vec = [list(i) for i in sents_vec]

    bert_df = pd.DataFrame({"sentence": sentence_list, "embedding": sents_vec})
    df = pd.concat([data, bert_df], axis=1)
    bert_features = pd.DataFrame(sents_vec)
    # 设置超参数（聚类数目K）搜索范围
    Ks = [i + 2 for i in  range(10)]
    CH_scores = []
    si_scores = []
    for K in Ks:
        ch, si = K_cluster_analysis(K, bert_features)
        CH_scores.append(ch)
        si_scores.append(si)
    # 绘制不同K对应的聚类的性能，找到最佳模型／参数（分数最高）
    plt.plot(Ks, np.array(CH_scores), 'b-', label='CH_scores')
    plt.savefig("calinski_score_xiaohongshu.png")
    plt.show()
    plt.plot(Ks, np.array(si_scores), 'b-', label='si_scores')
    plt.savefig("silhouette_score_xiaohongshu.png")
    plt.show()

    # 最佳超参数
    index = np.unravel_index(np.argmax(si_scores, axis=None), len(CH_scores))
    Best_K = Ks[index[0]]
    print("the best cluster find is {}".format(Best_K))
    mb_kmeans = MiniBatchKMeans(n_clusters=Best_K)
    y_pred = mb_kmeans.fit_predict(bert_features)
    # text = 
    # plot_tsne_scatter(text, labels)
    # 保存聚类结果
    feat_names_Kmeans = "Kmeans_" + str(Best_K)
    train_kmeans = pd.concat([pd.Series(name=feat_names_Kmeans, data=y_pred), df], axis=1)

    train_kmeans.to_csv("raw_data_clustered_xiaohongshu_2.csv", index=False)
