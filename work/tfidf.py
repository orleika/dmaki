# -*- coding: utf-8 -*-
from collections import namedtuple
from itertools import chain
from math import log
from collections import Counter
from pprint import pprint
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

class TfIdf:
    def __init__(self, dfs = []):
        self.dfs = dfs
        self.n = len(dfs)

    def new_keywords(self, tokens = [], size = 20):
        sorted_keywords = sorted(self.keywords(tokens), key = lambda t: t.tfidf, reverse = True)
        return [keyword.token for keyword in sorted_keywords][0:size]

    def tfidf(self, tf, df):
        return tf * (log(self.n / df) + 1)

    def keywords(self, tokens = []):
        tf = Counter()
        df = Counter()
        for d in self.dfs:
            df[d.word] = d.count
        for token in tokens:
            tf[token.word] += 1
            df[token.word] += 1
        keyword = namedtuple('Keyword', 'token, tfidf')
        tt = list(set(tokens))
        for token in tt:
            yield keyword(token, self.tfidf(tf[token.word], df[token.word]))

    @staticmethod
    def vector(docs):
        vectorizer = TfidfVectorizer(use_idf=True)
        return vectorizer.fit_transform(docs)

    @staticmethod
    def cluster(vector):
        return KMeans(n_clusters=2, random_state=0).fit_predict(vector)
