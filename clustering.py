# -*- coding: utf-8 -*-
"""
Created on Tue May  5 16:18:46 2020

@author: ТОМА
"""

import nltk, math, codecs
from gensim.models import Doc2Vec
from nltk.cluster.kmeans import KMeansClusterer
import re
import pandas as pd
from preprocessing import *
import numpy as np
from sklearn import metrics

from nltk.corpus import stopwords

fname = "mail.model"
model = Doc2Vec.load(fname)

file = "mail_list.csv"
df, used_lines, vectors=preprocess_dataset(file,model)

NUM_CLUSTERS=3
cluster_scores={}
for i in range(11):
    kclusterer = KMeansClusterer(i+2, distance=nltk.cluster.util.cosine_distance, repeats=25)
    assigned_clusters = kclusterer.cluster(vectors, assign_clusters=True)
    
    for cluster_id in kclusterer.cluster_names():
        df.loc[df.preprocessed_subject.isin(get_titles_by_cluster(cluster_id)),'cluster']=cluster_id
     
    score=metrics.silhouette_score(vectors,assigned_clusters, metric='euclidean')
    cluster_scores[i]=score

def get_titles_by_cluster(id):
    list = []
    
    for x in range(0, len(assigned_clusters)):
        if (assigned_clusters[x] == id):
            list.append(used_lines[x])
    return list

def get_topics(titles):
    from collections import Counter
    words = [preprocess_document(x) for x in titles]
    words = [word for sublist in words for word in sublist]
    filtered_words = [word for word in words if word not in stopwords.words('english')]
    count = Counter(filtered_words)
    print(count.most_common()[:5])


def cluster_to_topics(id):
    get_topics(get_titles_by_cluster(id))