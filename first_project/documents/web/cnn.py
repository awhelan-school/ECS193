#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,io,re
from collections import defaultdict
import html_process as hp
import formatting as fmt
import regex
import check
import urllib


def cnn(data_base,data_print,key,date_):

    kkey = fmt.file_name(key,'_')

    kkkey = fmt.file_name(key,'+')

    print("----- "+"cnn."+kkey+" -----")

    #case for exact keyword search
    url1='https://search.api.cnn.io/content?size=10&q=%22'
    url2='%22&category=opinion'
    baseurl = url1+key+url2

    try:
        page = hp.getHtml(baseurl)
    except urllib.error.URLError:
        pass

    article_number = regex.get_data('"meta":{\S+"of":(\d+),"maxScore',page)[0]
    if int(article_number) == 0:

        url1='https://search.api.cnn.io/content?size=10&q=%E2%80%9C'
        url2='%E2%80%9D&category=opinion'
        baseurl = url1+key+url2 

        try:
            page = hp.getHtml(baseurl)
        except urllib.error.URLError:
            print("CNN website is not correct, please check the code!")
            return -1

        article_number = regex.get_data('"meta":{\S+"of":(\d+),"maxScore',page)[0]

        if int(article_number) == 0:
            print("No CNN article was found by this key word")
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

        currenturl = url1+key+url2+'&from='+str(index)+'&page='+str(page_num)
        try:
            page = hp.getHtml(currenturl)
        except urllib.error.URLError:
            continue

        url = regex.get_data('"url":"([^,]+?.html)"\S"',page)
        title =  regex.get_data('"headline":"([^{]+?)"',page)
        author = regex.get_data('"byLine":(.+?),',page)

        for i in range(0,len(url)):

            d = regex.get_data('\S+\/(\d+\/\d+\/\d+)\S+',url[i])[0]
            d_int = int(re.sub(r'/', '', d))
            if date_ > d_int:
                reach_updated = True
                break

            if url[i] in data_base and kkey in data_base[url[i]]:
                continue

            if title[i] == []:
                continue

            try:
                html = hp.getHtml(url[i])
            except urllib.error.URLError:
                continue

            text2 = regex.get_data('<cite\sclass="el-editorial-source">\s\S\S\S\S\S</cite>([^=]*?)</p></div>',html[120000:])
            text1 = regex.get_data('<div\sclass="zn-body__paragraph\s*\w*">([^=]*)</div>?',html[120000:]) 

            text = text2+text1 

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
            data_print[url[i]]['source'] = fmt.formatted_source("CNN")
            # line 5
            data_print[url[i]]['url'] = fmt.formatted_url(url[i])
            # line 6
            data_print[url[i]]['date'] = fmt.formatted_date(re.sub(r'/', '-', d))
            # line 7
            author[i] = re.sub(r'"', '', author[i])[2:]
            if len(author[i]) < 3:
                author[i] = 'Noun Noun'
            authors = author[i].split(',')
            if len(authors) > 1:
                author[i] = ','.join(authors[:-1])

            data_print[url[i]]['author'] = fmt.formatted_author(author[i],',')
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
    cnn(data_base,data_print,'tax%20reform',0)   
    import output_file
    output_file.output(data_base)