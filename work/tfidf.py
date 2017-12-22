# -*- coding: utf-8 -*-
from collections import namedtuple
from itertools import chain
from math import log

class TfIdf:
    def __init__(self, df_list = []):
        self.df_list = df_list
        self.n = len(df_list)

    def new_keywords(self, tokens = [], size = 10):
        sorted_keywords = sorted(self.keywords(tokens), key = lambda t: t.tfidf, reverse = True)
        return [keyword.token for keyword in sorted_keywords][0:size]

    def tfidf(self, tf, df):
        return tf * (log(self.n / df) + 1)

    def keywords(self, tokens = []):
        df_list = self.df_list
        tf = {}
        df = {}
        for token in tokens:
            word = token.word
            try:
                tf[word] = tf[word] + 1
            except KeyError:
                tf[word] = 1
            if word in df_list:
                df[word] = 2
            else:
                df[word] = 1
        keyword = namedtuple('Keyword', 'token, tfidf')
        words = []
        for token in tokens:
            if not token.word in words:
                words.append(token.word)
                yield keyword(token, self.tfidf(tf[token.word], df[token.word]))
