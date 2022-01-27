import pickle

from clean_data_normies_1 import append_stats
from sklearn.model_selection import train_test_split
import csv
import pandas as pd
import pickle
import gensim
from gensim.models import Word2Vec
import networkx as nx
from collections import Counter
from gensim.parsing import PorterStemmer
import numpy as np

'''
This function creates the graph based on the word2vec model and wordcounts
'''
def graph_creation(df, w2v_model, limit=500):
    G = nx.Graph()
    
    global_stemmer = PorterStemmer()
    all_hashtags_flat = df['word'].tolist()
    hash_count = df['count'].tolist()
    print(all_hashtags_flat)
    hashtag_count = dict(zip(all_hashtags_flat,hash_count))
    #print(hashtag_count)
    hashtags_in_graph = []
    for k,v in hashtag_count.items():
        if v>limit:
            G.add_node(k, count=v)
            hashtags_in_graph.append(k)
    for hashtag_i in hashtags_in_graph:
        for hashtag_j in hashtags_in_graph:
            if hashtag_i!=hashtag_j:
                i_stem = global_stemmer.stem(hashtag_i)
                j_stem = global_stemmer.stem(hashtag_j)
                i_stem = hashtag_i
                j_stem = hashtag_j
                try:
                    similarities = w2v_model.wv.cosine_similarities(w2v_model.wv.get_vector(i_stem),
                                                                    np.array([w2v_model.wv.get_vector(j_stem),
                                                                              w2v_model.wv.get_vector(j_stem)]))
                except KeyError:
                    continue
                distance = 1 -similarities[0]
                if distance<0.3:
                    G.add_edge(hashtag_i, hashtag_j, weight=distance)
    return G
    
# Load data
data = csv.reader(open('lib/data/russian_doc.csv','r',encoding='utf8'),delimiter =',')
model_uni = Word2Vec.load('model_uni.bin')
# Load the unigram model
df3 = pd.read_csv('wordcount_unigram.csv')
# create the graph
russians_graph = graph_creation(df3, model_uni, limit=500)
#save the graph 
nx.write_gexf(russians_graph, "russians_hashtags_graph_uni_500.gexf")






