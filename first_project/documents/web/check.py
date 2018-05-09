# -*- coding: utf-8 -*-
import sys, io,re
import regex
from collections import defaultdict
import datetime


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
            date = regex.get_data('>\s(.+?)\s<',previous[i+5])[0]  

            data_base[url] = defaultdict(str)
            data_base[url][key] = date
            #data_base[url] = defaultdict(str)
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



