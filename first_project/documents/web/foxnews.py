#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,io,re
from collections import defaultdict
import html_process as hp
import formatting as fmt
import regex
import check
import urllib

def foxnews(data_base,data_print,key,date_):

    kkey = fmt.file_name(key,'_')

    print("----- "+"foxnews."+kkey+" -----")
    print("Start loading Urls...")


    #case for exact keyword search
    url1='http://api.foxnews.com/v1/content/search?q="'
    url2='"&fields=date,description,title,url,image,type,taxonomy&sort=latest&section.path=fnc/opinion&type=article&start='
    url3='&callback=angular.callbacks._0'
    baseurl = url1+key+url2+'0'+url3

    try:
        page = hp.getHtml(baseurl)
    except urllib.error.URLError:
        pass

    article_number = regex.get_data('"response"\S\S"numFound":(\S+),"docs":\S',page[0:2000])[0]

    if int(article_number) == 0:

        url1='http://api.foxnews.com/v1/content/search?q=""'
        url2='""&fields=date,description,title,url,image,type,taxonomy&sort=latest&section.path=fnc/opinion&type=article&start='
        url3='&callback=angular.callbacks._0'   
        baseurl = url1+key+url2+'0'+url3

        try:
            page = hp.getHtml(baseurl)
        except urllib.error.URLError:
            print("Foxnews website is not correct, please check the code!")
            return -1

        article_number = regex.get_data('"response"\S\S"numFound":(\S+),"docs":\S',page[0:2000])[0]

        if int(article_number) == 0:
            print("No Foxnews article was found by this key word")
            return -1

    #get all urls
    count = 0
    index = 0
    urls = {}
    page_total = int(article_number) / 10 + 1

    reach_updated = False

    print("There are "+article_number+" articles...")
    print("Start loading and Updating...")
    while(count < page_total):

        currenturl = url1+key+url2+str(index)+url3
        try:
            page = hp.getHtml(currenturl)
        except urllib.error.URLError:
            continue

        url = regex.get_data('url":\S"([^,]+?).html"\S',page)
        title =  regex.get_data('"title":"([^{]*?)",',page)

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

            len_html = len(html)
            author = regex.get_data('<meta\sname="dc.creator"\scontent="([^^]*?)">',html[0:2000])
            text = regex.get_data('<p.*?>([^\n]*?)</p>[^<]*?<[^/]',html[int(len_html/4):int(len_html/4*3)])
            text = text[:-1]

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
            data_print[url[i]]['source'] = fmt.formatted_source("Foxnews")
            # line 5
            data_print[url[i]]['url'] = fmt.formatted_url(url[i])
            # line 6
            data_print[url[i]]['date'] = fmt.formatted_date(re.sub(r'/', '-', d))
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
        count += 1
        print('■', end='', flush=True)


    print("\nThere are "+str(len(data_base)+len(data_print))+" articles...")
    print("Updated "+str(len(data_print))+" articles...")

if __name__ == "__main__":
    data_base = {}
    data_print = {}
    check.load_previous(data_base)
    date = check.check_date(data_base, 'tax_reform')
    foxnews(data_base,data_print,'tax%20reform',0)   
    import output_file
    output_file.output(data_base)