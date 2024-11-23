from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen, Request
import nltk
import nltk.corpus
from finvader import finvader
import pandas as pd
from nltk.tokenize import word_tokenize
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt
import numpy as np



tag = input('Enter company: ')
url = f"https://finviz.com/quote.ashx?t={tag}&p=d"


req = Request(url=url, headers={'user-agent': 'my-app'})
response = urlopen(req)
html = BeautifulSoup(response, "lxml")
news_table = html.find(id='news-table')

f = open('allnews.txt', "w")
news_dict = {}

if news_table:
    rows = news_table.find_all('tr')
 
    for row in rows:
        date_td = row.find('td', attrs={'width': '130', 'align': 'right'})
        if date_td:
            date = date_td.get_text(strip=True)

            title_tag = row.find('a') 
            if title_tag:
                title = title_tag.get_text(strip=True)

                if date not in news_dict:
                    news_dict[date] = []
                news_dict[date].append(title)


    positive = 0
    negative = 0
    neutral = 0
    for date, titles in news_dict.items():
        f.write(f"{date}: ")
        for title in titles:
            score = finvader(title, 
                            use_sentibignomics = True,
                            use_henry = True,
                            indicator = 'compound')
            if score > 0.1:
                sentiment = "positive"
                positive += 1
            elif score < 0:
                sentiment = "negative"
                negative += 1
            else:
                sentiment = "neutral"
                neutral += 1

            
            f.write(f"{title}, {sentiment}\n")


print(f"Number of positive news articles over the past 38 days: {positive}")   
print(f"Number of neutral news articles over the past 38 days: {neutral}")
print(f"Number of negative news articles over the past 38 days: {negative}")













