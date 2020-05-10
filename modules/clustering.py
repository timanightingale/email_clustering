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
from modules.preprocessing import *
import numpy as np
from sklearn import metrics

from nltk.corpus import stopwords


def get_titles_by_cluster(id,assigned_clusters,used_lines):
    list = []
    
    for x in range(0, len(assigned_clusters)):
        if (assigned_clusters[x] == id):
            list.append(used_lines[x])
    return list

def make_clusters(df,NUM_CLUSTERS):
    df, used_lines, vectors=preprocess_dataset(df,model)
    
    kclusterer = KMeansClusterer(NUM_CLUSTERS, distance=nltk.cluster.util.cosine_distance, repeats=25)
    assigned_clusters = kclusterer.cluster(vectors, assign_clusters=True)
    for cluster_id in kclusterer.cluster_names():
        df.loc[df.preprocessed_subject.isin(get_titles_by_cluster(cluster_id,assigned_clusters,used_lines)),'cluster']=cluster_id
    return df
     
#    score=metrics.silhouette_score(vectors,assigned_clusters, metric='euclidean')
#    cluster_scores[i]=score
    


