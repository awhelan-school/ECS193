#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, io
import codecs
import re
import regex
import datetime

def output(data_print, data_base):
    f = open("./documents/web/news.bank", 'a',encoding='utf-8')
    for i in data_print:
        index = 0
        for j in data_print[i]:
            if index < 9:
                output = re.sub(r'\\u\d+', ' ', data_print[i][j])
                output = re.sub(r'[ ]+', ' ', output)
                f.writelines(output)

            
            index += 1
        f.writelines('\n')


    index1 = 0
    f = open("./documents/web/Articles"+".bank", 'a',encoding='utf-8')
    for i in data_print:
        index2 = 0
        for j in data_print[i]:
            if index2 == 8:

                output = regex.get_data('<a>(.*?)<\/a>',data_print[i][j])[0]

                output = re.sub(r'\\u\d+', ' ', output)
                output = re.sub(r'[ ]+', ' ', output)

                f.writelines(output)
                f.writelines('\n')


            index2 += 1
        index1 += 1

    index1 = len(data_base)
    for i in data_print:
        f = open("./documents/web/article/Article_"+str(index1), 'w',encoding='utf-8')
        index2 = 0
        for j in data_print[i]:
            if index2 == 7:
                break

            output = re.sub('\s*<\S+?>\s*','', data_print[i][j])

            output = re.sub(r'\\u\d+', ' ', output)
            output = re.sub(r'[ ]+', ' ', output)
            f.writelines(output)
            f.writelines('\n')
            index2 += 1
        index1 += 1