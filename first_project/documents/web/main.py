#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
import sys
import cnn
import cbs
import foxnews

import output_file
import datetime
import check
import formatting as fmt

import subprocess


'tax reform,health reform, ...'


def web_scraper(input):
    
    key_words = input.split(',')

    data_base = {}
    data_print = {}
    keys = []

    dates = []
    check.load_previous(data_base)

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
        key = key[:-3]
        keys.append(key)
        dates.append(check.check_date(data_base, fmt.file_name(key,'_')))



    for i in range(0,len(keys)):
        cnn.cnn(data_base,data_print,keys[i],dates[i])   
        foxnews.foxnews(data_base,data_print,keys[i],dates[i])

        #cbs.cbs(data_base,data_print,keys[i],dates[i])
        #washington_post.washington_post(data_base,data_print,key,date)
        #print(data_print)

    output_file.output(data_print,data_base)
    print("Update date: "+str(datetime.datetime.now().date()) )


if __name__ == "__main__":
    # input = input('Enter your keyword: \n')
    input = sys.argv[1]
    web_scraper(input)

    exe = './documents/doc2vec.py'
    subprocess.Popen(['/Users/Whelan/anaconda3/bin/python3.6', exe])
