import feedparser
import justext
import pickle
import requests
import sys
import os.path
from collections import OrderedDict
from collections import defaultdict, Counter
from nltk.tokenize import word_tokenize
import numpy as np
import string
import time

# OrderDict[str, str]: map of id and raw text
news_data = OrderedDict()

# Dict[str, set]: maps term to set of ids of documents that contain term
inverted_index = defaultdict(set)

def load():
    """
    Loads the pickle file and sets news_data's value
    """
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "news.pickle"), 'rb') as f:
        news_data = pickle.load(f)

def get_data(index):
    """
    Returns the index from news_data which is the ordered dictionary.
    
    Returns
    -------
    tuple: (str, str)
        the first string is link
        the second string is the document
    """
    l = list(news_data.values())
    print(l)
    return l[index]

def save(database = news_data):
    """
    updates the database and uploads them to news.pickle
    
    Parameters
    ----------
    database: dict[str,]
        the first string has to be the link
    """
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "news.pickle"), 'wb') as f:
        pickle.dump(database, f, pickle.HIGHEST_PROTOCOL)

def remove(link, database):
    """
    removes the article with the following link.
    
    Parameters
    ----------
    link: str
    
    database: dict[str,]
        the first string has to be the link
    """
    if not link in news_data:
            raise KeyError("document with id [" + id + "] not found in index.")
    database.remove(link)
    save(database)

####################################
######### getting the text #########
####################################

def get_text(link):
    """
    Given an URL link, return the text for the stored article
    
    Parameter
    ---------
    link: str
        url to document
    """
    response = requests.get(link)
    paragraphs = justext.justext(response.content, justext.get_stoplist("English"))
    text = "\n\n".join([p.text for p in paragraphs if not p.is_boilerplate])
    return text

def collect(url, limit, filename="news.pickle"):
    """
    Saves the articles of an article into a pickle file that you can specify
    
    Parameters
    ----------
    url: str
        url to the document
    limit: int
        the number of articles
    filename: str
        path to the pickle file
    """
    # read RSS feed
    d = feedparser.parse(url)
    
    # grab each article
    for entry in d["entries"][:limit]:
        link = entry["link"]
        l = list(news_data.values())
        key = list(news_data.keys())
        if link in key:
            raise KeyError("document with id [" + id + "] found in index. No duplicate documents pls.")
        print("downloading: " + link)
        text = get_text(link)
        news_data[link] = text
        
    # pickle
    pickle.dump(news_data, open(filename, "wb"))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python collect_rss.py <url> <filename>")
        sys.exit(1)
    
    # https://www.reuters.com/tools/rss
    # http://feeds.reuters.com/Reuters/domesticNews
    url = sys.argv[1]
    filename = sys.argv[2]
    collect(url, filename)

