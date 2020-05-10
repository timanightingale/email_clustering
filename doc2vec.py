# -*- coding: utf-8 -*-
"""
Created on Tue May  5 16:15:36 2020

@author: ТОМА
"""

from nltk.corpus import stopwords
import logging
import re
from gensim.models.doc2vec import TaggedDocument, Doc2Vec
import pandas as pd
from preprocessing import *
from models import *
            
file = "mail_list.csv"
df=pd.read_csv(file)
df=df[~df.subject.isna()]
corpus = df
lines = df.subject.values
count = len(lines)
preprocessed = make_list(lines)

documents = Documents(preprocessed)

model = train_doc2vec(documents,10,size=100, dbow_words= 1, dm=0, iter=1, 
                      window=5, seed=1337, min_count=5, workers=4,alpha=0.025, min_alpha=0.025)
