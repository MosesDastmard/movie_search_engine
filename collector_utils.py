# Custom Functions

import os
import requests 
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
import random

# The following function takes as input the number (1, 2 or 3) of the raw html files provided to get the urls 
# and parse them in order to store the latters in a dictionary which will later be used to download data.

def get_urls(n):
    url = 'https://raw.githubusercontent.com/CriMenghini/ADM/master/2019/Homework_3/data/movies' + str(n) + '.html'
    response = requests.get(url)
    if str(response) == '<Response [200]>':
        url_soup = BeautifulSoup(response.text, 'html.parser')
        lst_a = url_soup.select('a')
        movies_dict = {}
        for movie in range(0, len(lst_a)):
            try:
                movie_id = 10000*n + int(movie) + 1 - 10000
                movie_url = lst_a[movie].text
                movies_dict[movie_id] = movie_url
            except:
                print('Found a strange piece of HTML')
        return(movies_dict)
    else:
        return('Something went wrong.')

# This function scrapes Wikipedia pages and save them as html files. We decided to specify just two of the
# possible response codes: the one occurring if the request is accepted and the one occurring if the limit
# is reached. The other cases comprise the circumstance of non-existing pages, so it sufficed using an else
# condition. Moreover, even though as input it can be specified the number of the article from which one
# wants to start (to avoid running from scratch in case of disconnection), an except was added as a further
# precaution to avoid blocks (it can happen to type the wrong number).

def scraping(movies_urls, k):
    try:
        os.makedirs('Htmls')
    except:
        _ = None
    # here we are iterating over each URL
    for i in tqdm(range(k, len(movies_urls.keys()) + 1)):
        # we read the HTML files and convert them into BeautifulSoup
        response = requests.get(movies_urls.get(i))
        if str(response) == '<Response [200]>':
            soup = BeautifulSoup(response.text, 'html.parser')
            try:
                f = open(r"Htmls\article_" + str(i) + ".html", "x")
                with open(r"Htmls\article_" + str(i) + ".html", "w", encoding='utf-8') as file:
                    file.write(str(soup))
                f.close()
                time.sleep(random.randint(1, 5))
            except:
                continue
        elif str(response) == '<Response [429]>':
            time.sleep(20 * 60)
        else: 
            continue
