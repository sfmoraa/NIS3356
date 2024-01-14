import numpy as np
from gensim.models import Word2Vec
from model.utils import *
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from gensim import corpora, models, similarities
import matplotlib.pyplot as plt

if __name__ == '__main__': 
    filename = "CrawlingStuff\CrawlResult\ZHIHU_如何评价张雪峰称文科都是服务业？.csv"
    data = process_csv(filename,with_labels=True)
    data['text'] = data['text'].apply(clean_text)
    data['tokens'] = data['text'].apply(tokenize)
    data['tokens'] = data['tokens'].apply(remove_stopwords)

    tokens = data['tokens'].tolist()
    id2word = corpora.Dictionary(tokens)
    corpus = [id2word.doc2bow(sentence) for sentence in tokens]

    coherence_values = []
    model_list = []
    for num_topics in range(2,41,2):
        lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                        id2word=id2word,
                        num_topics=num_topics,
                        # random_state=100,
                        # update_every=1,
                        # chunksize=100,
                        # passes=10,
                        # alpha='auto',
                        # per_word_topics=True
    )
        model_list.append(lda_model)
        coherencemodel = CoherenceModel(model=lda_model, texts=tokens, dictionary=id2word, coherence='u_mass')
        coherence_values.append(round(coherencemodel.get_coherence(),3))

    x = range(2,41,2)
    plt.plot(x, coherence_values)
    plt.xlabel("Num Topics")
    plt.ylabel("Coherence score")
    plt.legend(("coherence_values"), loc='best')
    # plt.savefig("plots/figures/LDALOSS.png")


    for m, cv in zip(x, coherence_values):
        print("Num Topics =", m, " has Coherence Value of", round(cv, 4))


    optimal_model = model_list[1]
    model_topics = optimal_model.show_topics(formatted=False)
    def format_topics_sentences(ldamodel, corpus, texts):
        # Init output
        sent_topics_df = pd.DataFrame()
        # Get main topic in each document
        for i, row in enumerate(ldamodel[corpus]):
            row = sorted(row, key=lambda x: (x[1]), reverse=True)
            # Get the Dominant topic, Perc Contribution and Keywords for each document
            for j, (topic_num, prop_topic) in enumerate(row):
                if j == 0: # => dominant topic
                    wp = ldamodel.show_topic(topic_num)
                    topic_keywords = ", ".join([word for word, prop in wp])
                    sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num),                 round(prop_topic,4), topic_keywords]), ignore_index=True)
                else:
                    break
        sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

        # Add original text to the end of the output
        contents = pd.Series(texts)
        # print(contents)
        sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
        # print(sent_topics_df)
        return(sent_topics_df)

    df_topic_sents_keywords = format_topics_sentences(ldamodel=optimal_model, corpus=corpus, texts=tokens)

    # Format
    df_dominant_topic = df_topic_sents_keywords.reset_index()
    df_dominant_topic.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text']

    # Show
    # df_dominant_topic.to_excel(path+'resultsdatas.xlsx',index=False)
    # print(df_dominant_topic.head(10))

    pd.options.display.max_colwidth = 100

    sent_topics_sorteddf_mallet = pd.DataFrame()
    sent_topics_outdf_grpd = df_topic_sents_keywords.groupby('Dominant_Topic')

    for i, grp in sent_topics_outdf_grpd:
        sent_topics_sorteddf_mallet = pd.concat([sent_topics_sorteddf_mallet,
    grp.sort_values(['Perc_Contribution'], ascending=False).head(1)],
    axis=0)

    # Reset Index
    sent_topics_sorteddf_mallet.reset_index(drop=True, inplace=True)

    # Format
    sent_topics_sorteddf_mallet.columns = ['Topic_Num', "Topic_Perc_Contrib", "Keywords", "Representative Text"]
    sent_topics_sorteddf_mallet.to_csv("results/LDA_4.csv")
    # Show
    print(sent_topics_sorteddf_mallet)

    df_dominant_topic = df_dominant_topic.dropna(axis=0)
    doc_lens = [len(d) for d in df_dominant_topic.Text]

    # Plot
    plt.figure(figsize=(16,7), dpi=160)
    plt.hist(doc_lens, bins = 1000, color='navy')
    plt.text(750, 100, "Mean : " + str(round(np.mean(doc_lens))))
    plt.text(750, 90, "Median : " + str(round(np.median(doc_lens))))
    plt.text(750, 80, "Stdev : " + str(round(np.std(doc_lens))))
    plt.text(750, 70, "1%ile : " + str(round(np.quantile(doc_lens, q=0.01))))
    plt.text(750, 60, "99%ile : " + str(round(np.quantile(doc_lens, q=0.99))))

    plt.gca().set(xlim=(0, 1000), ylabel='Number of Documents', xlabel='Document Word Count')
    plt.tick_params(size=16)
    plt.xticks(np.linspace(0,1000,9))
    plt.title('Distribution of Document Word Counts', fontdict=dict(size=22))
    plt.savefig("plots/figures/Word_Counts.png")
    # plt.show()

    import seaborn as sns
    import matplotlib.colors as mcolors
    cols = [color for name, color in mcolors.TABLEAU_COLORS.items()] # more colors: 'mcolors.XKCD_COLORS'

    fig, axes = plt.subplots(2,2,figsize=(16,14), dpi=160, sharex=True, sharey=True)

    for i, ax in enumerate(axes.flatten()):
        df_dominant_topic_sub = df_dominant_topic.loc[df_dominant_topic.Dominant_Topic == i, :]
        doc_lens = [len(d) for d in df_dominant_topic_sub.Text]
        ax.hist(doc_lens, bins = 1000, color=cols[i])
        ax.tick_params(axis='y', labelcolor=cols[i], color=cols[i])
        sns.kdeplot(doc_lens, color="black", shade=False, ax=ax.twinx())
        ax.set(xlim=(0, 1000), xlabel='Document Word Count')
        ax.set_ylabel('Number of Documents', color=cols[i])
        ax.set_title('Topic: '+str(i), fontdict=dict(size=16, color=cols[i]))

    fig.tight_layout()
    fig.subplots_adjust(top=0.90)
    plt.xticks(np.linspace(0,1000,9))
    fig.suptitle('Distribution of Document Word Counts by Dominant Topic', fontsize=22)
    plt.savefig("plots/figures/Word_Counts_dominatn_topics.png")
    # plt.show()