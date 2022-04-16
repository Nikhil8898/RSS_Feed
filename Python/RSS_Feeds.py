#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
#from bs4 import BeautifulSoup as bs
import urllib.request, urllib.parse, urllib.error


# In[2]:


pip install feedparser


# In[3]:


url="http://feeds.abcnews.com/abcnews/topstories"
#url="https://cointext.com/feeds"


# In[4]:


resp=requests.get(url)


# In[5]:


soup=BeautifulSoup(resp.content,features='xml')


# In[6]:


print(soup.prettify())


# In[7]:


items=soup.findAll('item')


# In[8]:


len(items)


# In[9]:


item = items[0]
item


# In[10]:


item.description.text


# In[11]:


news_items = []


# In[12]:



for item in items:
    news_item={}
    news_item['Title']=item.title.text
    news_item['Link']=item.link.text
    news_item['Description']=item.description.text
    #news_item['PubDate']=item.pubDate
    news_item['Category']=item.category.text
    news_items.append(news_item)


# In[13]:


news_items


# In[14]:


news_items[0]


# In[15]:


import pandas as pd


# In[16]:


df = pd.DataFrame(news_items)


# In[17]:


df.head(26)


# In[18]:


#df.to_csv('out1.csv')


# In[19]:


pip install pymongo


# In[20]:


import pymongo as pym
import os
import csv
import json


# In[31]:


#Making Connection with mongodb
client = pym.MongoClient('mongodb://localhost:27017/')
#creating db
db = client["rss_feeds"]
#creating tables
rss_feeds_table = db["feeds_info"]


# In[22]:


type(news_items)


# In[23]:


rss_feeds_dict= df.to_dict('list')
rss_feeds_dict


# In[29]:


rss_feeds_table.insert_one(rss_feeds_dict)


# In[ ]:




