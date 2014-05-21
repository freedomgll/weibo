#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2014-5-21
https://github.com/chineking/cola.git
'''

import urllib
import base64
import binascii
import re
import json

from cola.core.errors import DependencyNotInstalledError,\
                             LoginFailure

from cola.core.opener import MechanizeOpener
try:
    import rsa
except ImportError:
    raise DependencyNotInstalledError("rsa")

class WeiboLoginFailure(LoginFailure): pass

class WeiboLogin(object):
    def __init__(self, opener, username, passwd):
        self.opener = opener
        
        self.username = username
        self.passwd = passwd
        
    def get_user(self, username):
        username = urllib.quote(username)
        return base64.encodestring(username)[:-1]
    
    def get_passwd(self, passwd, pubkey, servertime, nonce):
        key = rsa.PublicKey(int(pubkey, 16), int('10001', 16))
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(passwd)
        passwd = rsa.encrypt(message, key)
        return binascii.b2a_hex(passwd)
    
    def prelogin(self):
        username = self.get_user(self.username)
        prelogin_url = 'http://login.sina.com.cn/sso/prelogin.php?entry=sso&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&client=ssologin.js(v1.4.15)' % username
        data = self.opener.open(prelogin_url)
        regex = re.compile('\((.*)\)')
        try:
            json_data = regex.search(data).group(1)
            data = json.loads(json_data)
            
            return str(data['servertime']), data['nonce'], \
                data['pubkey'], data['rsakv']
        except:
            raise WeiboLoginFailure
        
    def login(self):
        login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'
        
        try:
            servertime, nonce, pubkey, rsakv = self.prelogin()
            postdata = {
                'entry': 'weibo',
                'gateway': '1',
                'from': '',
                'savestate': '7',
                'userticket': '1',
                'ssosimplelogin': '1',
                'vsnf': '1',
                'vsnval': '',
                'su': self.get_user(self.username),
                'service': 'miniblog',
                'servertime': servertime,
                'nonce': nonce,
                'pwencode': 'rsa2',
                'sp': self.get_passwd(self.passwd, pubkey, servertime, nonce),
                'encoding': 'UTF-8',
                'prelt': '115',
                'rsakv' : rsakv,
                'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&amp;callback=parent.sinaSSOController.feedBackUrlCallBack',
                'returntype': 'META'
            }
            postdata = urllib.urlencode(postdata)
            text = self.opener.open(login_url, postdata)

            # Fix for new login changed since about 2014-3-28
            ajax_url_regex = re.compile('location\.replace\(\'(.*)\'\)')
            matches = ajax_url_regex.search(text)
            if matches is not None:
                ajax_url = matches.group(1)
                text = self.opener.open(ajax_url)
            
            regex = re.compile('\((.*)\)')
            json_data = json.loads(regex.search(text).group(1))
            result = json_data['result'] == True
            text = self.opener.open('http://s.weibo.com/weibo/%25E6%25AC%25A7%25E9%2598%25B3%25E5%25A8%259C%25E5%25A8%259C&page=3')
            print(text)
            file = open("testfile.txt","w")
            file.write(text)
            file.close()
            if result is False and 'reason' in json_data:
                return result, json_data['reason']
            return result
        except WeiboLoginFailure:
            return False

if __name__ == "__main__":
    login = WeiboLogin(MechanizeOpener(),'user','passwd')
    login.login()