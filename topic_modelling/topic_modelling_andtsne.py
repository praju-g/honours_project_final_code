# -*- coding: utf-8 -*-
import os
import re
import MeCab
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.manifold import TSNE
from wordcloud import WordCloud
import matplotlib.colors as mcolors
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
from gensim.models.coherencemodel import CoherenceModel
import math

from gensim import corpora
from gensim.models import LdaModel

# Author: Praju Ghatpande (2026)
# Code is used to model dataset using LDA and then output results as t-SNE graphs, word cloud and other infographics.

# Load all blog files
def load_texts_from_folder(folder_path):
    texts = []
    filenames = []
    count = 0
    
    for filename in os.listdir(folder_path):
        print("file: ", count) 
        # if count == 20:
        #     break
        with open(os.path.join(folder_path, filename), "r", encoding="utf-8") as f:
            text = f.read()
            texts.append(text)
            filenames.append(filename)
        count+=1
    return texts, filenames


# Clean & tokenise Japanese text 
def clean_japanese_text(text):
    """Remove punctuation, numbers, and symbols."""
    pattern = r"[0-9０-９!-/:-@[-`{-~、-〜“”‘’・。「」（）『』【】《》〈〉〔〕！？…￥ー]"
    text = re.sub(pattern, " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

mecab = MeCab.Tagger("-Owakati")

# Function to check POS info of text and only keep nouns
def extract_nouns(text):
    tagger = MeCab.Tagger('-r /dev/null -d /Users/praju/opt/anaconda3/lib/python3.9/site-packages/unidic/dicdir')

    node = tagger.parseToNode(text)

    list_noun = []

    while node:
        word = node.surface
        # print(node.feature)
        features = node.feature.split(",")

        #list_noun.append(word)
        # print(word, "\n")
        # print(features, "\nhellooo")
        if len(features) > 16:
            pos = features[0]
            if pos == '名詞' or pos == '動詞':
                
                list_noun.append(word)
        

        node = node.next
    # return " ".join(list_noun)
    return list_noun

def main():
    # Load folder  
    folder_path = "/Users/praju/Documents/honours/supervised readings/all_possible_data" 
    docs, filenames = load_texts_from_folder(folder_path)
    print("done loading docs\n")
    # Clean document and only extract nouns
    stop_words=['の', 'に', 'は', 'を', 'た', 'が', 'で', 'て', 'です', 'ます', 'そして', 'から', 'こと', 'よう', '今日','明日','自分', '日本', 'ある','いる','する','なる','し','い','月','日','いう','さ', 'あり', 'もの','年','なっ']

    noun_docs = [
        [word for word in extract_nouns(clean_japanese_text(doc))
        if word not in stop_words]
        for doc in docs
    ]

    print("noun docs made\n")

    
    dictionary = corpora.Dictionary(noun_docs)
    corpus = [dictionary.doc2bow(text) for text in noun_docs]

    n_list = [9,12,14,18]

    for n_topics in n_list:
        print(f"STARTING {n_topics} FULL RUN...\n")
        lda = LdaModel(
            corpus=corpus,
            id2word=dictionary,
            num_topics=n_topics,
            random_state=42,
            passes=10,  
            update_every=1
        )

        print("model done\n")
        

        def get_doc_topics(model, corpus, num_topics):
            matrix = np.zeros((len(corpus), num_topics))
            for i, doc in enumerate(corpus):
                for topic_num, prob in model[doc]:
                    matrix[i, topic_num] = prob
            return matrix

        topic_matrix = get_doc_topics(lda, corpus, n_topics)

        print("done making topic matrix\n")
        tsne_model = TSNE(n_components=2, perplexity=30, learning_rate='auto', init='pca', random_state=42)
        tsne_results = tsne_model.fit_transform(topic_matrix)

        print("now making graph\n")
        mycolors = np.array([color for name, color in mcolors.TABLEAU_COLORS.items()])
        dfts = pd.DataFrame(tsne_results, columns=['X', 'Y'])
        dfts['Dominant Topic'] = topic_matrix.argmax(axis=1)
        plt.figure(figsize=(8, 6))
        sns.scatterplot(
            x='X', y='Y', 
            hue='Dominant Topic', 
            palette=sns.color_palette("hls", n_topics), 
            data=dfts, 
            style=None,
            marker='o'
        )
        plt.title(f't-SNE plots of LDA {n_topics}')
        plt.xlabel('t-SNE Dimension 1')
        plt.ylabel('t-SNE Dimension 2')
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5),title='Dominant Topic')
        
        plt.savefig(f"tSNEplot {n_topics} topic.png", dpi=300, bbox_inches='tight')
        # plt.show()


        vis_data = gensimvis.prepare(lda, corpus, dictionary)

        # Export directly to an HTML file
        output_filename = f'{n_topics}-lda_gensim_output.html'
        pyLDAvis.save_html(vis_data, output_filename)
        
        # # lda = LdaModel(
        # #     corpus=corpus,
        # #     id2word=dictionary,
        # #     num_topics=n_topics,
        # #     random_state=42,
        # #     passes=10,  
        # #     update_every=1
        # # )

        # # print("model done\n")

        topic_info = []
        print("making topic info csv\n")
        for topic_id in range(n_topics):
            # Get top 10 keywords for the topic
            keywords = [word for word, prob in lda.show_topic(topic_id, topn=10)]
            
            # Use the keywords as the topic label
            label = ", ".join(keywords)

            topic_info.append({
                "label": topic_id,
                "keywords": label
            })

        # Create DataFrame
        df_topic_info = pd.DataFrame(topic_info)

        # Save to CSV
        df_topic_info.to_csv(f"{n_topics}_topic_info.csv", index=False)



        rows = []

        for i, bow in enumerate(corpus):
            topic_probs = lda.get_document_topics(bow, minimum_probability=0)
            
            # Topic with highest probability
            dominant_topic, probability = max(topic_probs, key=lambda x: x[1])
            
            rows.append({
                "filename": filenames[i],
                "dominant_topic": dominant_topic,
                "topic_probability": probability
            })

        # Create DataFrame
        df_topics = pd.DataFrame(rows)

        # Save to CSV
        df_topics.to_csv(f"{n_topics}_topics_sortfiles.csv", index=False)

        print(df_topics.head())

        print("making word clouddd\n")

        cols = [color for name, color in mcolors.TABLEAU_COLORS.items()]  # more colors: 'mcolors.XKCD_COLORS'
        topics = lda.show_topics(formatted=False, num_words=20, num_topics=)
        cloud = WordCloud(stopwords=stop_words,
                        background_color='white',
                        width=2500,
                        height=1800,
                        max_words=20,
                        colormap='tab10',
                        font_path = './ipaexm00401/ipaexm.ttf',
                        color_func=lambda *args, **kwargs: cols[i],
                        prefer_horizontal=1.0)

        ncols = 3
        nrows = math.ceil(len(topics) / ncols)
        fig, axes = plt.subplots(
            nrows,
            ncols,
            figsize=(15, 5 * nrows),
            sharex=True,
            sharey=True
        )

        axes = axes.flatten()

        for i, topic in enumerate(topics):
            topic_words = dict(topic[1])

            cloud.generate_from_frequencies(
                topic_words,
                max_font_size=300
            )

            axes[i].imshow(cloud)
            axes[i].set_title(f'Topic {i}', fontsize=16)
            axes[i].axis('off')
        for ax in axes[len(topics):]:
            ax.axis('off')

        # fig, axes = plt.subplots(nrows, ncols, figsize=(15,5 * nrows), sharex=True, sharey=True)

        # for i, ax in enumerate(axes.flatten()):
        #     fig.add_subplot(ax)
        #     topic_words = dict(topics[i][1])
        #     cloud.generate_from_frequencies(topic_words, max_font_size=300)
        #     plt.gca().imshow(cloud)
        #     plt.gca().set_title('Topic ' + str(i), fontdict=dict(size=16))
        #     plt.gca().axis('off')

        print("done word cloud\n")

        plt.tight_layout()


        fig.savefig(
            f'wordcloud_{n_topics}_topics.png',
            dpi=300,
            bbox_inches='tight'
        )

        # plt.subplots_adjust(wspace=0, hspace=0)
        # plt.axis('off')
        # plt.margins(x=0, y=0)
        # plt.tight_layout()
        # plt.savefig(f"Word Cloud {n_topics} topic noun and verb.png",dpi=300)
        # #plt.show()


if __name__ == "__main__":
    main()
