# -*- coding: utf-8 -*-
from collections import namedtuple
from itertools import chain
from math import log
from collections import Counter
from pprint import pprint

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
