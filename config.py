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

# Dict[str, str]: maps document id to original/raw text
raw_text = {}

# Dict[str, Counter]: maps document id to term vector (counts of terms in document)
term_vectors = {}

# Counter: maps term to count of how many documents contain term
doc_freq = Counter()


# Dict[str, set]: maps term to set of ids of documents that contain term
inverted_index = defaultdict(set)

def load():
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "news.pickle"), 'rb') as f:
        news_data = pickle.load(f)

def save():
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "face_data.pickle"), 'wb') as f:
        pickle.dump(news_data, f, pickle.HIGHEST_PROTOCOL)

def remove(link):
    if not link in news_data:
            raise KeyError("document with id [" + id + "] not found in index.")
    news_data.remove(link)

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
        if link in news_data.keys():
            raise KeyError("document with id [" + id + "] found in index. No duplicate documents pls.")
        print("downloading: " + link)
        text = get_text(link)
        news_data[link] = text
        
        # tokenize
        tokens = tokenize(text)
        
        # create term vector for document (a Counter over tokens)
        term_vector = Counter(tokens)
        
        # store term vector for this doc id
        term_vectors[link] = term_vector
        
        # update inverted index by adding doc id to each term's set of ids
        for term in term_vector.keys():
            inverted_index[term].add(link)
        
        # update document frequencies for terms found in this doc
        # i.e., counts should increase by 1 for each (unique) term in term vector
        doc_freq.update(term_vector.keys())
        
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

