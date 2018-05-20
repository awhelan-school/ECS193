# -*- coding: utf-8 -*-
import sys, io,re
import regex
from collections import defaultdict
import datetime
import json


def update_key(data_base, url,kkey):
    keys_saved = regex.get_data('<key>\s(.+?)\s<',data_base[url]['key'])

    if kkey not in keys_saved:
        data_base[url]['key'] = data_base[url]['key'][:-1]
        data_base[url]['key'] += ' <key> ' + kkey + ' <\key>\n'
        return True

    return False

def check_date(data_base,key_word):
    date = 0

    for url in data_base:
        for key in data_base[url]:
            if key_word == key:
                try:
                    d = int(re.sub(r'-', '', data_base[url][key]))
                    if date < d:
                        date = d
                except ValueError:
                    continue


    if date != 0:
        date = str(date)
        year = int(date[0:4])
        if date[4] != '0':
            month = int(date[4:6])
        elif date[4] == '0':
            month = int(date[5])
        if date[6] != '0':
            day = int(date[6:8])
        elif date[6] == '0':
            day = int(date[7])



        date = (datetime.date(year, month, day) - datetime.timedelta(1)).isoformat()
        return  int(re.sub(r'-', '', date))
    else:
        return 0

def load_keywords_info():
    try:
        with open('./documents/web/keywords.json', 'r') as fp:
            data = json.load(fp)
            return data
    except json.decoder.JSONDecodeError:
        return defaultdict(str)


def save_keywords_info(data):
    with open('./documents/web/keywords.json', 'w') as fp:
        json.dump(data, fp)


def load_url_info():
    try:
        with open('./documents/web/urls.json', 'r') as fp:
            data = json.load(fp)
            return data
    except json.decoder.JSONDecodeError:
        return defaultdict(list)


def save_url_info(data):
    with open('./documents/web/urls.json', 'w') as fp:
        json.dump(data, fp)

def load_previous(data_base):
    previous = []
    try:
        file = open("./documents/web/news.bank","r",encoding='utf8');
        for line in file:
            previous.append(line)



        i = 0
        while i < len(previous):

            url = regex.get_data('>\s(.+?)\s<',previous[i+4])[0]
            key = regex.get_data('>\s(.+?)\s<',previous[i+1])[0]
            #date = regex.get_data('>\s(.+?)\s<',previous[i+5])[0]

            data_base[key].append(url)

            #data_base[url][key] = date
            #data_base[url] = defaultdict(str)
            #data_base[id]['id'] = previous[i]
            #data_base[key]['key'] = previous[i]
            #data_base[url]['title'] = previous[i+1]
            #data_base[url]['source'] = previous[i+2]
            #data_base[url]['url'] = previous[i+3]
            #data_base[url]['date'] = previous[i+4]
            #data_base[url]['author'] = previous[i+5]
            #data_base[url]['content1'] = previous[i+6]
            #data_base[url]['content2'] = previous[i+7]

            i += 10


    except FileNotFoundError:
        pass

def check_last_update(url,date):
    count = 0
    for u in url:
        d = regex.get_data('\S+\/(\d+\/\d+\/\d+)\S+',u)[0]
        d = int(re.sub(r'/', '', d))
        if d < date:
            return count

        count += 1

    return -1


def MinEditDist(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]
