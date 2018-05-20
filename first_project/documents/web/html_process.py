#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request
import http.cookiejar
from urllib3 import PoolManager

def login(username,password):
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))

    payload = urllib.parse.urlencode({"username": username,
                                  "password": password,
                                  "redirect": "index.php",
                                  "sid": "",
                                  "login": "Login"}).encode("utf-8")
    response = opener.open('https://subscribe.washingtonpost.com/loginregistration/index.html#/register/group/long?action=login&destination=https:%2F%2Fwww.washingtonpost.com%2F%3Fnid&rememberme=true', payload)
    content = response.read()

def getHtml(url):
    #head = {}
    #head['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'

    r = urllib.request.urlopen(url)
    content = r.read()
    html = content.decode('utf-8')

    return html

def set_pool():
  http_pool = PoolManager(maxsize=10,block=True)
  return http_pool


def getHtml_pool(url,http_pool):
    #head = {}
    #head['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'

    r = http_pool.urlopen('GET', url)
    content = r.read()
    html = content.decode('utf-8')

    return html
