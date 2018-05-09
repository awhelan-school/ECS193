#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,io,re
from collections import defaultdict
import html_process as hp
import formatting as fmt
import regex
import check
import urllib


def cbs(data_base,data_print,key,date_):

    kkey = fmt.file_name(key,'_')

    kkkey = fmt.file_name(key,'+')

    print("----- "+"cbs."+kkey+" -----")
    print("Start loading Urls...")


    #case for exact keyword search
    url1 = 'https://www.cbsnews.com/search/?q='
    url2 = '&o=1&p='
    url3 = '&t=opinion'
    baseurl = url1+kkkey+url2+'1'+url3

    try:
        page = hp.getHtml(baseurl)
    except urllib.error.URLError:
        pass

    article_number = regex.get_data('<h1\sclass="result-title">(\d+)\s',page)[0]

    if int(article_number) == 0:

        url1 = 'https://www.cbsnews.com/search/?q="'
        url2 = '"&o=1&p='
        url3 = '&t=opinion'
        baseurl = url1+kkkey+url2+'1'+url3

        try:
            page = hp.getHtml(baseurl)
        except urllib.error.URLError:
            print("CBS website is not correct, please check the code!")
            return -1

        article_number = regex.get_data('<h1\sclass="result-title">(\d+)\s',page)[0]

        if int(article_number) == 0:
            print("No CBS article was found by this key word")
            return -1

    #get all urls
    count = 0
    index = 0
    page_num = 1
    urls = {}
    page_total = int(article_number) / 10 + 1

    reach_updated = False

    print("There are "+article_number+" articles...")
    print("Start loading and Updating...")
    while(count < page_total):

        currenturl = url1+key+url2+str(page_num)+url3
        try:
            page = hp.getHtml(currenturl)
        except urllib.error.URLError:
            continue

        url = regex.get_data('<a\shref="(\S+?)"><h3\sclass="title"',page)
        date = regex.get_data('<span\sclass="date">(\S+\s\d+,\s\d+)\s\S+\s\S+\s\S+</span>',page)
        title =  regex.get_data('>([^<]*?)<\/h3><\/a>',page)

        #print(currenturl)

        for i in range(0,len(url)):

            d_int = fmt.convert_date(date[i])
            if date_ > d_int:
                reach_updated = True
                break

            url[i] = 'https://www.cbsnews.com' + url[i]

            if url[i] in data_base and kkey in data_base[url[i]]:
                continue

            if title[i] == []:
                continue

            try:
                html = hp.getHtml(url[i])
            except urllib.error.URLError:
                continue

            author = regex.get_data('"author":{".type":"[^"]+","name":"([^"]+?)"}',html)
            text1 = regex.get_data('<div\sdata-page=[^>]+><[^>]*>\n?(.+?)<.?p>',html) 
            text2 = regex.get_data('<p>([^\n]+?)<\/p>',html) 
            text = text1+text2

            if text == []:
                continue

            data_print[url[i]] = defaultdict(str)
            # line 1
            data_print[url[i]]['ID'] = fmt.formatted_id(len(data_base)+len(data_print)-1)
            # line 2
            data_print[url[i]]['key'] = fmt.formatted_key(kkey)
            # line 3
            data_print[url[i]]['title'] = fmt.formatted_title(title[i])
            # line 4
            data_print[url[i]]['source'] = fmt.formatted_source("CBS")
            # line 5
            data_print[url[i]]['url'] = fmt.formatted_url(url[i])
            # line 6
            data_print[url[i]]['date'] = fmt.formatted_date(str(d_int)[0:4]+'-'+str(d_int)[4:6]+'-'+str(d_int)[6:8])
            # line 7
            if author == []:
                author = 'Noun Noun'
            data_print[url[i]]['author'] = fmt.formatted_author(author[0],',')
            # line 8
            data_print[url[i]]['content1'] = fmt.formatted_content_with_symbol(text)
            # line 9
            data_print[url[i]]['content2'] = fmt.formatted_content(text)

        if reach_updated:
            break

        index += 10
        page_num += 1
        count += 1
        print('■', end='', flush=True)


    print("\nThere are "+str(len(data_base)+len(data_print))+" articles...")
    print("Updated "+str(len(data_print))+" articles...")

if __name__ == "__main__":
    data_base = {}
    data_print = {}
    check.load_previous(data_base)
    date = check.check_date(data_base, 'tax_reform')
    cbs(data_base,data_print,'health%20reform',0)   
    import output_file
    output_file.output(data_base)