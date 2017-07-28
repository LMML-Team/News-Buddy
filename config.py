import feedparser
import justext
import pickle
import requests
import sys
import os.path
from collections import OrderedDict
from collections import defaultdict, Counter
import nltk
from nltk.tokenize import word_tokenize
import numpy as np
import string
import time

# OrderDict[]:
news_data = OrderedDict()
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
    texts = {}
    for entry in d["entries"][:limit]:
        link = entry["link"]
        if not link in raw_text:
            raise KeyError("document with id [" + id + "] not found in index.")
        print("downloading: " + link)
        text = get_text(link)
        texts[link] = text
        news_data[link] = text
    
    # pickle
    pickle.dump(texts, open(filename, "wb"))

############################################
############## organize terms ##############
############################################

def tokenize(text):
    """ Converts text into tokens (also called "terms" or "words").

            This function should also handle normalization, e.g., lowercasing and 
            removing punctuation.

            For example, "The cat in the hat." --> ["the", "cat", "in", "the", "hat"]

            Parameters
            ----------
            text: str
                The string to separate into tokens.

            Returns
            -------
            list(str)
                A list where each element is a token.

        """
    # Hint: use NLTK's recommended word_tokenize() then filter out punctuation
    # It uses Punkt for sentence splitting and then tokenizes each sentence.
    # You'll notice that it's able to differentiate between an end-of-sentence period 
    # versus a period that's part of an abbreviation (like "U.S.").

    # tokenize
    tokens = word_tokenize(text)

    # lowercase and filter out punctuation (as in string.punctuation)
    return [token.lower() for token in tokens if not token in string.punctuation]

def get_matches_OR(terms):
    """ Returns set of documents that contain at least one of the specified terms.

            Parameters
            ----------
            terms: iterable(str)
                An iterable of terms to match on, e.g., ["cat", "hat"].

            Returns
            -------
            set(str)
                A set of ids of documents that contain at least one of the term.
        """
    # initialize set of ids to empty set
    ids = set()

    # union ids with sets of ids matching any of the terms
    for term in terms:
        ids.update(inverted_index[term])

    return ids

def get_matches_AND(terms):
    """ Returns set of documents that contain all of the specified terms.

            Parameters
            ----------
            terms: iterable(str)
                An iterable of terms to match on, e.g., ["cat", "hat"].

            Returns
            -------
            set(str)
                A set of ids of documents that contain each term.
        """ 
    # initialize set of ids to those that match first term
    ids = inverted_index[terms[0]]

    # intersect with sets of ids matching rest of terms
    for term in terms[1:]:
        ids = ids.intersection(inverted_index[term])

        return ids

def get_matches_NOT(terms):
    """ Returns set of documents that don't contain any of the specified terms.

            Parameters
            ----------
            terms: iterable(str)
                An iterable of terms to avoid, e.g., ["cat", "hat"].

            Returns
            -------
            set(str)
                A set of ids of documents that don't contain any of the terms.
        """
    # initialize set of ids to all ids
    ids = set(raw_text.keys())

    # subtract ids of docs that match any of the terms
    for term in terms:
        ids = ids.difference(inverted_index[term])

    return ids

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python collect_rss.py <url> <filename>")
        sys.exit(1)
    
    # https://www.reuters.com/tools/rss
    # http://feeds.reuters.com/Reuters/domesticNews
    url = sys.argv[1]
    filename = sys.argv[2]
    collect(url, filename)

