# -*- coding: utf-8 -*-
"""
Created on Wed May  6 13:19:30 2020

@author: ТОМА
"""
import re
from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import emoji
import string
import pandas as pd

def check_emoji(line):
    emoji_=''.join(emoji.UNICODE_EMOJI.keys())
    emoji_flag=sum([i in emoji_ for i in line])>0
    return emoji_flag

def check_capslock(line):
    capslock_flag=len(re.findall(r'[A-Z][A-Z][A-Z]+',line))>1
    return capslock_flag

def preprocess(line):
    remove_list=string.punctuation
    remove_list+=''.join(emoji.UNICODE_EMOJI.keys())
    translator = str.maketrans(remove_list, ' '*len(remove_list), '')
    line=line.translate(translator)
    line=re.sub(r'http(s)?:\/\/\S*? ', " ", line)
    this_stopwords=set(stopwords.words())
    line = ' '.join(filter(lambda l: l not in this_stopwords, line.split(' ')))
    #line=' '.join([i if i not in stopwords.words() else '' for i in line.split(' ') ])
    
    line=line.lower()
    return line
def preprocess_dataset(filename,model):
    df=pd.read_csv(filename)
    df=df[~df.subject.isna()]
    df.emoji=df.subject.apply(lambda x:int(check_emoji(x)))
    df.capslock=df.subject.apply(lambda x:int(check_capslock(x)))
    df.loc[0,'preprocessed_subject']=0
    df.preprocessed_subject=df.subject.apply(lambda x:preprocess(x))
    lines = df.preprocessed_subject.values
    vectors, used_lines =infering_vectors(lines,model)
    df.loc[0,'cluster']=0
    return df, used_lines, vectors

class Documents(object):
    def __init__(self, documents):
        self.documents = documents

    def __iter__(self):
        for i, doc in enumerate(self.documents):
            yield TaggedDocument(words = doc, tags = [i])
            
            
def make_list(lines):
    preprocessed = []
    
    duplicate_dict = {}
    
    for t in lines:
        if t not in duplicate_dict:
            duplicate_dict[t] = True
            t = preprocess(t)
            fixed =''.join([x if x.isalnum() or x.isspace() else " " for x in t ])
            preprocessed.append(fixed)
    return preprocessed

def preprocess_document(text):
    text = preprocess(text)
    return ''.join([x if x.isalnum() or x.isspace() else " " for x in text ]).split()

def infering_vectors(lines,model):
    vectors = []

    print("inferring vectors")
    duplicate_dict = {}
    used_lines = []
    for i, t in enumerate(lines):
        if t not in duplicate_dict:
            duplicate_dict[t] = True
            used_lines.append(t)
            vectors.append(model.infer_vector(preprocess_document(t)))
    
    print("done")
    return vectors, used_lines