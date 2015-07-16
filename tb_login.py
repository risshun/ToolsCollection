# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 18:23:37 2015

@author: DannyVim
"""

import urllib
import urllib2
import cookielib
import re
import webbrowser
import sys

#处理中文输出
reload(sys)
sys.setdefaultencoding('utf-8')

class tb:
    def __init__(self):
        self.loginURL = 'https://login.taobao.com/member/login.jhtml'
        self.headers = {
            'Host':'login.taobao.com',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36',
            'Referer': 'https://login.taobao.com/member/login.jhtml',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection':'Keep-Alive'
            }
        self.username = ''
        self.ua = ''
        self.password2 = ''
        self.tid = ''
        self.gvfdcre = ''
        # 抓包获得各项信息
        #self.reurl = ''
        self.post = post = {
            'ua':self.ua,
            'TPL_username':self.username,
            'TPL_password':'',
            'TPL_checkcode':'',
            'loginsite':'0',
            'newlogin':'0',
            'TPL_redirect_url':self.reurl,
            'from':'tbTop',
            'fc':'default',
            'style':'default',
            'css_style':'',
            'tid':self.tid,
            'support':'000001',
            'CtrlVersion':'1,0,0,7',
            'loginType':'3',
            'minititle':'',
            'minipara':'',
            'umto':'T4d12d362cb6eb8a3ec58b8cd5854c5ed',
            'pstrong':'3',
            'llnick':'',
            'sign':'',
            'need_sign':'',
            'isIgnore':'',
            'full_redirect':'',
            'popid':'',
            'callback':'',
            'guf':'',
            'not_duplite_str':'',
            'need_user_id':'',
            'poy':'',
            'gvfdcname':'10',
            'gvfdcre':self.gvfdcre,
            'from_encoding':'',
            'sub':'',
            'TPL_password_2':self.password2,
            'loginASR':'1',
            'loginASRSuc':'1',
            'allp':'',
            'oslanguage':'zh-cn',
            'sr':'1366*768',
            'osVer':'windows|6.1',
            'naviVer':'chrome|40.02214115'
        }
        self.postData = urllib.urlencode(self.post)
        self.cookie = cookielib.LWPCookieJar()
        self.ckhandler = urllib2.HTTPCookieProcessor(self.cookie)
        self.opener = urllib2.build_opener(self.ckhandler,urllib2.HTTPHandler)
        
    def needcheckcode(self):
        request = urllib2.Request(self.loginURL,self.postData,self.headers)
        response = self.opener.open(request)
        content = response.read().decode('gbk')
        status = response.getcode()
        if status == 200:
            print 'apply successfully.'
            pattern = re.compile(u'\u8bf7\u8f93\u5165\u9a8c\u8bc1\u7801',re.S)
            result = re.search(pattern,content)
            if result:
                print u'需要输入验证码，TAT'
                return content
            else:
                tokenPattern = re.compile('id="J_HToken"')
                tokenMatch = re.search(tokenPattern,content)
                if tokenMatch:
                    print u'安全通过，无需验证码'
                    return False
        else:
            print u'aplly failed.'
            return None
            
    def getcode(self,page):
        pattern = re.compile('<img id="J_StandardCode_m.*?data-src="(.*?)"',re.S)
        matchResult = re.search(pattern,page)
        if matchResult and matchResult.group(1):
            print matchResult.group(1)
            return matchResult.group(1)
        else:
            print u'获取验证码信息失败'
            return False
            
    def loginwithcode(self):
        checkcode = raw_input('请输入验证码：')
        self.post['TPL_checkcode'] = checkcode
        self.postData = urllib.urlencode(self.post)
        try:
            request = urllib2.Request(self.loginURL,self.postData,self.headers)
            response = self.opener.open(request)
            content = response.read().decode('gbk')
            pattern = re.compile(u'\u9a8c\u8bc1\u7801\u9519\u8bef',re.S)           
            result = re.search(pattern,content)
            if result:
                print 'Wrong Check Code'
                return False
            else:
                tokenPattern = re.compile('id="J_HToken" value="(.*?)"')
                tokenMatch = re.search(tokenPattern,content)
                if tokenMatch:
                    print 'code is right'
                    print tokenMatch.group(1)
                    return tokenMatch.group(1)
                else:
                    print u'J_Token获取失败'
                    return False
        except urllib2.HTTPError, e:
            print u'服务器连接错误，错误原因', e.reason
            return False
            
    def main(self):
        needcheck = self.needcheckcode()
        if not needcheck == None:
            if not needcheck == False:
                print u'需要手动输入验证码'
                checkcode = self.getcheckcode(needcheck)
                if not checkcode == False:
                    print 'get checkcode successfully.'
                    print u'在浏览器中输入验证码'
                    webbrowser.open_new_tab(checkcode)
                    J_HToken = self.loginwithcode
                    print 'J_HToken',J_HToken
                else:
                    print u'获取验证码失败，请重试'
            else:
                print u'不需要输入验证码'
        else:
            print u'请求登录页面失败'
            
            
tb = tb()
tb.main()