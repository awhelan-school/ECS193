#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, io
import codecs
import re
import regex
import datetime


def output(data_print, data_base, previous_len):

    f = open("./documents/web/Articles.bank", 'a',encoding='utf-8')
    for i in data_print:
        index = 0
        for j in data_print[i]:
            if index == 7:

                #output = regex.get_data('<a>(.*?)<\/a>',data_print[i][j])[0]

                output = re.sub(r'\\u\d+', ' ', data_print[i][j])
                output = re.sub(r'[ ]+', ' ', output)

                f.writelines(output)
                #f.writelines('\n')

            index += 1

    index1 = previous_len
    for i in data_print:
        f = open("./documents/web/articles/Article_"+str(index1), 'w',encoding='utf-8')
        index2 = 0
        for j in data_print[i]:
            if index2 == 8:
                break

            #output = re.sub('\s*<\S+?>\s*','', data_print[i][j])

            output = re.sub(r'\\u\d+', ' ', data_print[i][j])
            output = re.sub(r'[ ]+', ' ', output)
            f.writelines(output)
            index2 += 1
        index1 += 1

    '''
    f = open("news.bank", 'a',encoding='utf-8')
    for i in data_print:
        index = 0
        for j in data_print[i]:
            if index < 9:
                output = re.sub(r'\\u\d+', ' ', data_print[i][j])
                output = re.sub(r'[ ]+', ' ', output)
                f.writelines(output)


            index += 1
        f.writelines('\n')


    index1 = len(data_base)

    for i in data_print:
        f = open("article\Article"+str(index1)+".bank", 'w',encoding='utf-8')
        index2 = 0
        for j in data_print[i]:
            if index2 == 7:
                break

            output = re.sub(r'\\u\d+', ' ', data_print[i][j])
            output = re.sub(r'[ ]+', ' ', output)
            f.writelines(output)
            index2 += 1
        index1 += 1

    index1 = 0
    f = open("onlyArticles"+".bank", 'a',encoding='utf-8')
    for i in data_print:
        index2 = 0
        for j in data_print[i]:
            if index2 == 7:
                output = re.sub(r'\\u\d+', ' ', data_print[i][j])
                output = re.sub(r'[ ]+', ' ', output)
                f.writelines(output)


            index2 += 1
        index1 += 1
    '''
