# -*- coding: utf-8 -*-
"""
Created on Wed May  6 13:21:31 2020

@author: ТОМА
"""
from gensim.models.doc2vec import TaggedDocument, Doc2Vec
def train_doc2vec(documents,epochs,
        size=100, dbow_words= 1, dm=0, iter=1,  window=5, 
        seed=1337, min_count=5, workers=4,alpha=0.025, 
        min_alpha=0.025):
    count=len(documents.documents)
    model = Doc2Vec(size=size, dbow_words= dbow_words, dm=dm, iter=iter, 
        window=window, seed=seed, min_count=min_count, 
        workers=workers,alpha=alpha, min_alpha=min_alpha)
    model.build_vocab(documents)
    for epoch in range(epochs):
        print("epoch "+str(epoch))
        model.train(documents, total_examples=count, epochs=1)
        model.save('mail.model')
        model.alpha -= 0.002  # decrease the learning rate
        model.min_alpha = model.alpha
    return model
    
