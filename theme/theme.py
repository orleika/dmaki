# -*- coding: utf-8 -*-
from gsearch import GoogleScrapy
from clean import Clean
from stopword import StopWord
from tokenizer import MeCabTokenizer
from tfidf import TfIdf
from db import DB
from pprint import pprint

class Theme:

    def __init__(self, theme):
        self.theme = theme

    @staticmethod
    def search_articles(keywords):
        search_word = ' '.join(keywords)
        google = GoogleScrapy(search_word)
        google.start()
        return google.articles

    @staticmethod
    def tokenize(sentence):
        tokenizer = MeCabTokenizer(user_dic_path = '/usr/local/lib/mecab/dic/mecab-ipadic-neologd')
        clean = Clean(sentence)
        cleaned = clean.clean_text()
        tokens = tokenizer.extract_noun_verbs_baseform(cleaned.text)
        return tokens

    @staticmethod
    def tokenize_surface(sentence):
        return [token.surface for token in tokenize(sentence)]

    @staticmethod
    def clean(sentence):
        return Clean(sentence).clean_html_and_js_tags().clean_text().clean_code()

    @staticmethod
    def trimmed_stopwords(tokens):
        db = DB(host = 'mysql')
        stopwords = db.get_stopwords()
        sw = StopWord(tokens = tokens, stopwords = [stopword.word for stopword in stopwords])
        return sw.remove_stopwords()

    @staticmethod
    def divide(articles):
        return articles.split(r'(?<=[。．？！])')

    # input: keywords
    # output: articles
    def search():
        return

    # input: articles
    # output: [[nouns, verb][...]...]
    def extract_noun():
        return

    # input: sentences,
    def clustering():
        return

    def get(self):
        # standardize
        keywords = self.trimmed_stopwords(self.tokenize(self.theme))
        # search about theme
        articles = self.search_articles([keyword.surface for keyword in keywords][:3])
        # clean
        docs = map(self.clean, articles)
        # pprint(docs)
        return docs
        # divide sentences
        # sentences = divide(docs)
        # tfidf format
        # sentence_tokens = map(' '.join, map(tokenize_surface, sentences))


