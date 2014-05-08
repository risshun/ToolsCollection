# -*- coding: utf-8 -*-
"""
这是一个用以获取用户豆瓣数据的爬虫，使得用户可以进行数据的本地备份。
支持：
1.豆瓣电影，豆瓣读书【暂不支持】
2.csv文件为逗号分割符文件【暂不支持】。

@author: DannyVim
"""
import urllib2 as ur
from bs4 import BeautifulSoup as bs
import sys
import time


#BASE URL
def basepage(wa):
    m_wish='http://movie.douban.com/people/'+user+'/wish?start='
    m_do='http://movie.douban.com/people/'+user+'/do?start='
    m_collect='http://movie.douban.com/people/'+user+'/collect?start='
    if wa=='do':
        baseurl=m_do
    elif wa=='wish':
        baseurl=m_wish
    elif wa=='collect':
        baseurl=m_collect
    link_list(baseurl)

#知道目录下有多少页,并且打开每一页获取数据
def link_list(pageurl):
    info=ur.urlopen(pageurl)
    soup=bs(info)
    try:
        t=soup.find('span',class_='thispage')['data-total-page']
    except TypeError:
        content(pageurl)
    else:
        n=0
        t=int(t)-1
        for i in range(t):
            pagelist=pageurl+str(n)
            content(pagelist)
            n=n+15
            #显示程序运行进度，但是这个只在CMD中有效OTZ
            percent = 1.0 * i / t * 100
            print 'complete percent:' + str(percent) + '%',
            sys.stdout.write("\r")
            time.sleep(0.1)
        
#利用bs4库把静态的网页解析出来并挑选有用数据
def content(html):
    info=ur.urlopen(html)
    soup=bs(info)
    for tag in soup.body(attrs={'class':'item'}):
        datum=open('datum.txt','a+')
        title=tag.em.string.strip()
        url=tag.li.a.get('href')
        date=tag.find('span',class_='date').get_text()
        comment=tag.find('span',class_='comment')
        if comment==None:
            comment=''
        else:
            comment=comment.get_text()
        comment=comment.encode('utf-8')
        title=title.encode('utf-8')
        url=url.encode('utf-8')
        date=date.encode('utf-8')
        print >> datum,url,'  ',date,'  ','《',title,'》','  ',comment
        datum.close()
    

#运行
print '这是一个用以获取用户豆瓣数据的爬虫，使得用户可以进行数据的本地备份。'
user=raw_input('Please input your DB user name:')
wanted=raw_input('Please input what you want to sync:(do,wish,collect)')

    
basepage(wanted)



    



