# -*- coding: utf-8 -*-
from gscrapy import GoogleScrapy
from clean import Clean
from stopword import StopWord
from tokenizer import MeCabTokenizer
from tfidf import TfIdf
from pprint import pprint
from itertools import chain
from db import DB

def search_articles(keywords, end = 1):
    search_word = ' '.join([keyword.word for keyword in keywords])
    pprint(search_word)
    google = GoogleScrapy(search_word, end = end)
    google.start()
    return google.articles

def tokenize(articles):
    results = []
    tokenizer = MeCabTokenizer(user_dic_path = '/usr/local/lib/mecab/dic/mecab-ipadic-neologd')
    for article in articles:
        clean = Clean(article.html)
        cleaned = clean.clean_html_and_js_tags().clean_text().clean_code()
        tokens = tokenizer.extract_noun_baseform(cleaned.text)
        results.append(tokens)
    return list(chain.from_iterable(results))

def trimmed_stopwords(db, tokens):
    stopwords = db.get_stopwords()
    sw = StopWord(tokens = tokens, stopwords = [stopword.word for stopword in stopwords])
    return sw.remove_stopwords()

def extract_keywords(db, tokens):
    dfs = db.get_dfs()
    tfidf = TfIdf(dfs)
    return tfidf.new_keywords(tokens)

def update_dfs(db, tokens):
    for token in tokens:
        db.save_df(token.word)

def save_new_keywords(db, keyword, tokens):
    for token in tokens:
        if not db.exist_word(token.word):
            pos= 1 if token.pos == '名詞' else 2
            db.save(token.word, keyword.layer + 1, pos, keyword.id)

def main():
    db = DB(host = 'mysql')
    keywords = db.max_layer_words()
    for keyword in keywords:
        if keyword.layer != 1:
            articles = search_articles([keyword, db.parent_word(keyword.word)], 3)
        else:
            articles = search_articles([keyword], 3)
        tokens = tokenize(articles)
        trimmed_tokens = trimmed_stopwords(db, tokens)
        new_keywords = extract_keywords(db, trimmed_tokens)
        update_dfs(db, trimmed_tokens)
        save_new_keywords(db, keyword, new_keywords)

if __name__ == '__main__':
    main()
