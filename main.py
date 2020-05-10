# -*- coding: utf-8 -*-
"""
Created on Sun May 10 15:56:47 2020

@author: ТОМА
"""

from modules.imap import *
from modules.clustering import *
from modules.doc2vec import *

email="ursol.toma@gmail.com"
password="WeWeWe11"
clusters=2

mail=create_connection(email,password)
df=load_data(mail,5000)
model=get_doc2vec(df)
df=make_clusters(df,clusters)
move_mail(df)
