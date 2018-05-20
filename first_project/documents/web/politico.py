#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,io,re
from collections import defaultdict
import html_process as hp
import formatting as fmt
import regex
import check
import urllib


def politico(data_base,data_print,key,date_,previous_len):

    kkey = fmt.file_name(key,'_')

    kkkey = fmt.file_name(key,'+')

    print("----- "+"politico."+kkey+" -----")

    # https://www.politico.com/search/2?s=newest&q=tax%20reform&adv=true&c=0000014b-324d-d4f3-a3cb-f3ff415e0035&pv=0000014e-a307-d012-a3fe-bb8793910000
    url1 = 'https://www.politico.com/search/'
    url2 = '?s=newest&q="'
    url3 = '"&adv=true&c=0000014b-324d-d4f3-a3cb-f3ff415e0035&pv=0000014e-a307-d012-a3fe-bb8793910000'
    baseurl = url1+'1'+url2+key+url3
    article_number = '0'

    try:
        page = hp.getHtml(baseurl)  
    except urllib.error.URLError:
        print("Politico website is not correct, please update the scraper!")
        return -1

    article_number = regex.get_text('<h1>Results[^<]+?<\/h1>[^<]+?<p>(\d+?)\sSearch\sResults<\/p>',page)[0]

    if int(article_number) == 0:
        print("No Policito article was found by this key word")
        return -1


    #get all urls
    count = 0
    page_num = 1
    urls = defaultdict(str)
    page_total = int(int(article_number) / 20 + 1)

    reach_updated = False

    print("There are "+article_number+" articles...")
    print("Start loading URLs...")

    while(count < page_total):

        currenturl = url1+str(page_num)+url2+key+url3
        try:
            page = hp.getHtml(currenturl)
        except urllib.error.URLError:
            continue

        url = regex.get_text('<a\shref="([^"]+?)"\s[^<]+?<\/a><\/h3>',page)
        date = regex.get_text('<time datetime=.(\d+?\-\d+?\-\d+?)T\S+.>[^<]+?<\/time><\/p>',page)
        
        #title =  regex.get_data('"title":"([^{]*?)",',page)
        for cnt in range(0,len(date)):
            date[cnt] = int(re.sub(r'-', '', date[cnt]))
            if date_ > date[cnt]:
                reach_updated = True
                break



        for i in range(0,cnt+1):
            try:
                urls[url[i]] = str(date[i])[0:4]+'-'+str(date[i])[4:6] +'-'+str(date[i])[6:8]
            except IndexError:
                break
           
        if reach_updated:
            break

        page_num += 1
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

        title = regex.get_data('<title>([^-]+?)\s-\s[^<]+?<\/title>',html)
        if title == 'None':
            title = regex.get_data('<title>([^<]+?)<\/title>',html)

        author = regex.get_data('<div\sitemprop="author"[^>]+?>[^<]+?<meta\s[^<]+?\s[^"]+?="([^>]+?)"\/>',html)

        text = regex.get_text('<p>([^\n]*?)</p>',html) 

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
        data_print[url]['source'] = fmt.formatted_source("Politico")
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
    politico(data_base,data_print,'tax%20reform',date,0)   
