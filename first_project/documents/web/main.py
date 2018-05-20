#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
import sys, re
import cnn
import cbs
import foxnews
import politico
#import washington_post
import output_file
import datetime
import check
import formatting as fmt
import subprocess

def web_scraper(input):

    key_words = input.split(',')
    keys = []
    #dates = []



    time = str(datetime.datetime.now().date())

    for key_word in key_words:
        try:
            while(key_word[0] == ' '):
                key_word = key_word[1:]
            while(key_word[len(key_word)-1] == ' '):
                key_word = key_word[:-1]
        except IndexError:
            continue

        if(len(key_word) == 0):
            continue

        inputs = key_word.split(' ')
        key = ''
        for i in inputs:
            key += i
            key += '%20'
        key = key[:-3].lower()
        key = re.sub(r'[ ]+',' ',key)
        keys.append(key)
        #dates.append(check.check_date(data_base, kkeys[i]))


    for i in range(0,len(keys)):

        previous_len = 0
        try:
            for lines in open("./documents/web/Articles.bank", 'r',encoding='utf-8'):
                previous_len += 1
        except FileNotFoundError:
            pass

        stored_keys = check.load_keywords_info()
        data_base = check.load_url_info()
        data_print = {}

        kkey = fmt.file_name(keys[i],'_')

        for kk in stored_keys:
            if abs(len(kkey) - len(kk)) < 2 and check.MinEditDist(kkey, kk) == 1:
                kkey = kk

        if kkey in stored_keys:
            date = int(re.sub(r'-', '', stored_keys[kkey]))
        else:
            date = 0


        stored_keys[kkey] = time


        if kkey not in data_base:
            data_base[kkey] = []


        cnn.cnn(data_base,data_print,keys[i],date,previous_len)
        foxnews.foxnews(data_base,data_print,keys[i],date,previous_len)
        cbs.cbs(data_base,data_print,keys[i],date,previous_len)
        politico.politico(data_base,data_print,keys[i],date,previous_len)
        #washington_post.washington_post(data_base,data_print,key,date)

        if len(data_print) > 1:
            check.save_keywords_info(stored_keys)
            check.save_url_info(data_base)
        output_file.output(data_print,data_base,previous_len)


    print("Update date: "+time)


if __name__ == "__main__":
    try:
        input = sys.argv[1]
        print("Loading keywords...")
    except IndexError:
        input = input('Enter your keyword: \n')
    web_scraper(input)

    exe = './documents/doc2vec.py'
    subprocess.Popen(['python3', exe])
