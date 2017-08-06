from collections import defaultdict, Counter
import nltk
from nltk.tokenize import word_tokenize
import numpy as np
import string
import time
import config as cf
import entity_database as ed


class MySearchEngine:
    def __init__(self):
        # Dict[str, str]: maps document id to original/raw text
        self.raw_text = dict(cf.load)
        
        # Dict[str, Counter]: maps document id to term vector (counts of terms in document)
        self.term_vectors = {}
        
        # Counter: maps term to count of how many documents contain term
        self.doc_freq = Counter()
        
        # Dict[str, set]: maps term to set of ids of documents that contain term
        self.inverted_index = defaultdict(set)
        
    def idf(self, term):
        """ Returns current inverse document frequency weight for a specified term.
        
            Parameters
            ----------
            term: str
                A term.
            
            Returns
            -------
            float
                The value idf(t, D) as defined above.
        """ 
        return np.log10(self.num_docs() / (1.0 + self.doc_freq[term]))
    
    def dot_product(self, tv1, tv2):
        """ Returns dot product between two term vectors (including idf weighting).
        
            Parameters
            ----------
            tv1: Counter
                A Counter that contains term frequencies for terms in document 1.
            tv2: Counter
                A Counter that contains term frequencies for terms in document 2.
            
            Returns
            -------
            float
                The dot product of documents 1 and 2 as defined above.
        """
        # iterate over terms of one document
        # if term is also in other document, then add their product (tfidf(t,d1) * tfidf(t,d2)) 
        # to a running total
        result = 0.0
        for term in tv1.keys():
            if term in tv2:
                result += tv1[term] * tv2[term] * self.idf(term) ** 2
        return result
    
    def length(self, tv):
        """ Returns the length of a document (including idf weighting).
        
            Parameters
            ----------
            tv: Counter
                A Counter that contains term frequencies for terms in the document.
            
            Returns
            -------
            float
                The length of the document as defined above.
        """
        result = 0.0
        for term in tv:
            result += (tv[term] * self.idf(term)) ** 2
        result = result ** 0.5
        return result
    
    def cosine_similarity(self, tv1, tv2):
        """ Returns the cosine similarity (including idf weighting).

            Parameters
            ----------
            tv1: Counter
                A Counter that contains term frequencies for terms in document 1.
            tv2: Counter
                A Counter that contains term frequencies for terms in document 2.
            
            Returns
            -------
            float
                The cosine similarity of documents 1 and 2 as defined above.
        """
        return self.dot_product(tv1, tv2) / (self.length(tv1) * self.length(tv2))
    
    def query(self, q, k=10):
        """ Returns up to k documents matching at least one term in query q, sorted by relevance.
        
            Parameters
            ----------
            q: str
                A string containing words to match on, e.g., "cat hat".
            
            k: int (default = 10)
                Max number of documents returned
        
            Returns
            -------
            List(tuple(str, float))
                A list of (document, score) pairs sorted in descending order.
        """
        # tokenize query
        # note: it's very important to tokenize the same way the documents were so that matching will work
        query_tokens = self.tokenize(q)
        
        # get matches
        # just support OR for now...
        ids = self.get_matches_OR(query_tokens)
                
        # convert query to a term vector (Counter over tokens)
        query_tv = Counter(query_tokens)
        
        # score each match by computing cosine similarity between query and document
        scores = [(id, self.cosine_similarity(query_tv, self.term_vectors[id])) for id in ids]
        scores = sorted(scores, key=lambda t: t[1], reverse=True)

        # sort results and return top k
        return scores[0:k]
