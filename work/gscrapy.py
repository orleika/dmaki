# -*- coding: utf-8 -*-
import os
from collections import namedtuple
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

SearchResultRow = namedtuple(
    'SearchResultRow',
    ['title', 'url', 'display_url', 'dis']
)

ArticleResultRow = namedtuple(
    'ArticleResultRow',
    ['html']
)

os.environ['MOZ_HEADLESS'] = '1'

def get_text_or_none(element, num):
    try:
        return element[num].text
    except IndexError:
        return ''

class GoogleScrapy:
    def __init__(self, keyword, end=1, default_wait=5):
        self.url = 'https://www.google.co.jp?pws=0&tbs=qdr:w'
        self.keyword = keyword
        self.end = end
        self.default_wait = default_wait
        self.driver = None
        self.searches = []
        self.articles = []

    def enter_keyword(self):
        self.driver.get(self.url)
        self.driver.find_element_by_id('lst-ib').send_keys(self.keyword)
        self.driver.find_element_by_id('lst-ib').send_keys(Keys.RETURN)

    def next_page(self):
        self.driver.find_element_by_css_selector('a#pnnext').click()
        time.sleep(self.default_wait)

    def get_search(self):
        all_search = self.driver.find_elements_by_class_name('rc')
        for data in all_search:
            title = data.find_element_by_tag_name('h3').text
            url = data.find_element_by_css_selector(
                'h3 > a').get_attribute('href')
            display_url = data.find_element_by_tag_name('cite').text
            try:
                dis = data.find_element_by_class_name('st').text
            except NoSuchElementException:
                dis = ''
            result = SearchResultRow(title, url, display_url, dis)
            self.searches.append(result)

    def get_article(self):
        for search in self.searches:
            self.driver.get(search.url)
            self.driver.implicitly_wait(self.default_wait)
            try:
                html = self.driver.execute_script("return document.body.innerHTML")
            except NoSuchElementException:
                html = ''
            result = ArticleResultRow(html)
            self.articles.append(result)

    def start(self):
        try:
            self.driver = webdriver.Firefox()
            self.driver.implicitly_wait(self.default_wait)
            self.enter_keyword()
            self.get_search()
            self.get_article()
        finally:
            self.driver.quit()
