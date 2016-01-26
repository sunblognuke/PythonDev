#!/usr/bin/env python
# coding: utf-8

import os
import sys
import re
import shutil
import urllib
import requests
import datetime
import config, tool, Utils
from pyquery import PyQuery
from model import ArticleModel, Article
from peewee import *

reload(sys)
sys.setdefaultencoding('utf-8')

# 本地存储根目录
BASE_DIR = u"E:/data/Python/"

BASE_URL = 'http://www.liaoxuefeng.com' 

class Page():
    def __init__ (self, url, articleElem):
        self.url = url
        self.articleElem = articleElem

    def fetch(self):
        self.html = self._fetch_html()
        self.elements = self._get_elements()
        self.items = [self._gen_item(element) for element in self.elements.items()]

    def _fetch_html(self):
        r = requests.get(self.url, headers=config.HEADERS)
        # r.encoding = 'gb2312'
        return r.text

    def _get_elements(self):
        d = PyQuery(self.html)
        return d(self.articleElem) 

    def _gen_item(self, element):
        item = Article()
        item.url = self.url 
        item.title = element.find('h4').text()
        item.author = u'廖雪峰'#element.find('').text()
        item.category = 'Dev'
        item.tags = 'Python'
        contentWrapper = element.find('.x-wiki-content')#.remove('.postComment')
        item.summary = tool.Tool().replace2(contentWrapper.outerHtml().encode('utf-8'))
        item.crawl_time = datetime.datetime.now()

        return item

def buildURLs(indexUrl, elem):
    	urls = []
    	if(elem == ''):
    		urls.append(indexUrl)
    		return urls

        try:
        	d = PyQuery(indexUrl, headers=config.HEADERS)
        	base_url = getHostName(indexUrl)
        	for item in d(elem):
        		href = d(item).attr('href')
        		if href.startswith('http'):
        			urls.append(href)
        		else:     
        			urls.append(base_url + href)
        except requests.ConnectionError as e:
            print("Network Error")
        except requests.exceptions.RequestException as e:
            print("Error")

	return urls

def getHostName(url):
    proto, rest = urllib.splittype(url)
    host, rest = urllib.splithost(rest)

    return 'http://' + host

def crawl(indexUrl = '', 
          baseDir = BASE_DIR,
          listElem = 'a', 
          itemElem = ''):
    """crawl all pages and save detail urls to database"""
    print 'start crawl url: %s' % indexUrl
    urls = buildURLs(indexUrl, listElem)

    for url in urls:
    	if url:
	        p = Page(url, itemElem)
	        try:
	            print('fetching ' + p.url)
	            p.fetch()
	        except requests.ConnectionError as e:
	            print("Network Error")
	        print('{} items found'.format(len(p.items)))
	        for item in p.items:
	            print item
	            item.save_to_db()

    list = ArticleModel.select().where(ArticleModel.tags == 'Python')
    i = 0
    for item in list:
        content = Utils.replace_charentity(item.summary)
        content = content.replace(r'src="', 'src="' + BASE_URL)
        i +=1

        # 要转一下码，不然加到路径里就悲剧了
    	title = item.title.decode('utf-8').replace("/", " ")
        fileName = "%d " % i + title + '.html'
        
        base_folder = baseDir
        tool.FileUtils().mkdir(base_folder)
        filePath = base_folder + fileName
        if os.path.exists(filePath):
            os.remove(filePath)
            print("removing {}".format(fileName))
            # print("skipping {}".format(fileName))
            continue

        try:
            with open(filePath, 'wb') as f:
                f.write('<!DOCTYPE html>')
                f.write('<head>')
                f.write('<meta content="text/html; charset=UTF-8" http-equiv="Content-Type" />') # advoid wrong decoding
                f.write('</head>')
                f.write('<body>')
                f.write(content.decode('utf-8'))
                f.write('</body>')
                f.write('</html>')
                f.flush()
        except requests.ConnectionError as e:
            print("Network Error")
        except requests.exceptions.RequestException as e:
            print("Error")

if __name__ == '__main__':
    # baseUrl = 'http://www.liaoxuefeng.com'
    crawl(indexUrl = 'http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000', 
          baseDir = u'E:/data/Python/',
          listElem = '.x-sidebar-left-content .uk-nav-side li a', 
          itemElem = '.x-content')