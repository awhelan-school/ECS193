#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,io,re
from collections import defaultdict
import html_process as hp
import formatting as fmt
import regex
import check
import urllib

def foxnews(data_base,data_print,key,date_,previous_len):

    kkey = fmt.file_name(key,'_')

    print("----- "+"foxnews."+kkey+" -----")
    print("Start loading Urls...")


    #case for exact keyword search
    url1='http://api.foxnews.com/v1/content/search?q="'
    url2='"&fields=date,description,title,url,image,type,taxonomy&sort=latest&section.path=fnc/opinion&type=article&start='
    url3='&callback=angular.callbacks._0'
    baseurl = url1+key+url2+'0'+url3
    article_number = '0'

    try:
        page = hp.getHtml(baseurl)
    except urllib.error.URLError:
        print("Foxnews website is not correct, please update the scraper!")
        return -1

    article_number = regex.get_text('"response"\S\S"numFound":(\S+),"docs":\S',page)[0]
    
    if int(article_number) == 0:
        print("No Foxnews article was found by this key word")
        return -1

    #get all urls
    count = 0
    index = 0
    urls = defaultdict(str)
    page_total = int(int(article_number) / 10 + 1)

    reach_updated = False

    print("There are "+article_number+" articles...")
    print("Start loading and Updating...")

    while(count < page_total):

        currenturl = url1+key+url2+str(index)+url3
        try:
            page = hp.getHtml(currenturl)
        except urllib.error.URLError:
            continue

        url = regex.get_text('url":\S"(\S+?)"\S',page)
        #title =  regex.get_data('"title":"([^{]*?)",',page)

        for i in range(0,len(url)):
            try:
                d = regex.get_data('\/(\d+\/\d+\/\d+)',url[i])
            except IndexError:
                break
            d_int = int(re.sub(r'/', '', d))

            if date_ > d_int:
                reach_updated = True
                break

            urls[url[i]] = re.sub(r'/', '-', d)

           
        if reach_updated:
            break

        index += 10
        count += 1

    print(str(len(urls)) + " URLs loaded...")
    print("Updating database...")

    for url in urls:
        if url in data_base[kkey]:
            continue

        try:
            html = hp.getHtml(url)
        except urllib.error.URLError:
            continue

        title = regex.get_data('<meta\sname="dc.title"\scontent="([^=]+?)">',html)
        author = regex.get_data('<meta\sname="dc.creator"\scontent="([^"]+?)">',html)

        text = regex.get_text('<p[^>]*?>([^\n]*?)</p>[^<]*?<[^/]',html) 
        if text != []:
            text = text[:-1]

        if text == [] or title == "Noun":
            continue

        data_base[kkey].append(url)

        data_print[url] = defaultdict(str)
        # line 1
        data_print[url]['ID'] = fmt.formatted_id(len(data_base[kkey])-1+previous_len)
        # line 2
        data_print[url]['key'] = fmt.formatted_key(kkey)
        # line 3
        data_print[url]['title'] = fmt.formatted_title(title)
        # line 4
        data_print[url]['source'] = fmt.formatted_source("Foxnews")
        # line 5
        data_print[url]['url'] = fmt.formatted_url(url)
        # line 6
        data_print[url]['date'] = fmt.formatted_date(urls[url])
        # line 7
        data_print[url]['author'] = fmt.formatted_author(author,',')
        # line 8
        data_print[url]['content'] = fmt.formatted_content(text)
        # line 9
        #data_print[url[i]]['content2'] = fmt.formatted_content(text)

        print('■', end='', flush=True)

    print("\nThere are "+str(len(data_print)+previous_len)+" articles...")
    print("Updated "+str(len(data_print))+" articles...")


if __name__ == "__main__":
    data_base = {}
    data_print = {}
    check.load_previous(data_base)
    date = check.check_date(data_base, 'tax_reform')
    foxnews(data_base,data_print,'tax%20reform',0)   
    import output_file
    output_file.output(data_base)