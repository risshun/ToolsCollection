# -*- coding: utf-8 -*-
"""
爬取伯尔尼德语词汇表

@author: DannyVim
"""
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

baseurl = 'https://www.berndeutsch.ch'
url = baseurl + '/web/words/index/page:'

#单词与解释的存储列表
w_list= []
m_list= []

#抓取词汇表页面
def page(url,num):
    demo = requests.get(url).content
    soup = bs(demo,'lxml')
    list=soup.find('tbody')
    for wd in list.find_all('tr'):
        num += 0.1
        print(num)
        wurl = wd.td.a.get('href')
        word = wd.td.a.text
        mean = wd.td.next_sibling.next_sibling.text.strip()
        if '...' in mean:
            mean = word_mean(wurl)
        w_list.append(word)
        m_list.append(mean)

#补充不完整的解释
def word_mean(u):
    wurl = baseurl + u
    word_content = requests.get(wurl).content
    soup = bs(word_content, 'lxml')
    true_mean = soup.dl.next_sibling.next_sibling.dd.text.strip()
    return true_mean

#主程序
for i in range(1,792):
    print(i)
    page_url = url + str(i)
    page(page_url,i)

#构造Series输出为xlsx
berndemo = pd.Series(m_list,index=w_list, name = 'Erklärung')
#berndemo.to_csv('bernlist.csv', index=True, sep=',', encoding='utf8')
berndemo.to_excel('bernlist.xlsx',sheet_name='berndeutsch', index_label = 'Wort')