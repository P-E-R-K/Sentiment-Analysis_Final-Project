# -*- coding: utf-8 -*-
"""Data Scrapper for Googleplay - Final Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18yNOb4lgn05JmNrYEFl8l0X96f1nkjFx

# Import Module / Library
"""

!pip install google-play-scraper

from google_play_scraper import Sort, reviews_all
import pandas as pd

"""# Scrapping

## Shopee
"""

scraper = reviews_all('com.shopee.id', #ID aplikasi
                         lang='id',
                         country='id',
                         sort=Sort.MOST_RELEVANT,
                         filter_score_with=None
                         )

#print(scraper)
app_reviews_df = pd.DataFrame(scraper)

app_reviews_df.head()

app_reviews_df.to_csv('review_shopee.csv',index=None, header=True)



"""## Tokopedia"""

Review_Tokopedia = reviews_all('com.tokopedia.tkpd', #ID aplikasi
                         lang='id', # defaults to ‘en’
                         country='id', # defaults to ‘us’
                         sort=Sort.MOST_RELEVANT, # defaults to Sort.MOST_RELEVANT
                         filter_score_with=None # defaults to None (means all score)
                         )

review_tokped = pd.DataFrame(Review_Tokopedia)

review_tokped.head()

review_tokped.to_csv('review_tokopedia.csv',index=None, header=True)



"""## Lazada"""

scrapper_Lazada = reviews_all('com.lazada.android', #ID aplikasi
                         lang='id', # defaults to ‘en’
                         country='id', # defaults to ‘us’
                         sort=Sort.MOST_RELEVANT, # defaults to Sort.MOST_RELEVANT
                         filter_score_with=None # defaults to None (means all score)
                         )

#print(Review_Lazada)
lazada = pd.DataFrame(scrapper_Lazada)

lazada.head()

lazada.to_csv('review_lazada.csv',index=None, header=True)



"""## Bukalapak"""

Scrapper_Bukalapak = reviews_all('com.bukalapak.android', #ID aplikasi
                         lang='id', # defaults to ‘en’
                         country='id', # defaults to ‘us’
                         sort=Sort.MOST_RELEVANT, # defaults to Sort.MOST_RELEVANT
                         filter_score_with=None # defaults to None (means all score)
                         )

#print(Review_Bukalapak)
review_bukalapak = pd.DataFrame(Scrapper_Bukalapak)

review_bukalapak.head()

review_bukalapak.to_csv('review_bukalapak.csv',index=None, header=True)

