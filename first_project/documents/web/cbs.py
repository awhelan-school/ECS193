#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,io,re
from collections import defaultdict
import html_process as hp
import formatting as fmt
import regex
import check
import urllib


def cbs(data_base,data_print,key,date_,previous_len):

    kkey = fmt.file_name(key,'_')

    kkkey = fmt.file_name(key,'+')

    print("----- "+"cbs."+kkey+" -----")
    print("Start loading Urls...")

    kkkey = re.sub(r'/', '%2F', kkkey)
    #kkkey = re.sub(r'+', '%2B', kkkey)

    kkkey = re.sub(r'%', '%25', kkkey)


    #case for exact keyword search
    url1 = 'https://www.cbsnews.com/search/?q='
    url2 = '&o=1&p='
    url3 = '&t=opinion'
    baseurl = url1+kkkey+url2+'1'+url3
    article_number = '0'

    try:
        page = hp.getHtml(baseurl)
    except urllib.error.URLError:
        print("CBS website is not correct, please check the code!")
        return -1

    try:
        article_number = regex.get_text('<h1\sclass="result-title">(\d+)\s',page)[0]
    except IndexError:
        article_number = '0'

    if int(article_number) == 0:
        print("No CBS article was found by this key word")
        return -1

    #get all urls
    count = 0
    index = 0
    page_num = 1
    urls = defaultdict(str)
    page_total = int(int(article_number) / 10 + 1)

    reach_updated = False

    print("There are "+article_number+" articles...")
    print("Start loading and Updating...")
    while(count < page_total):

        currenturl = url1+key+url2+str(page_num)+url3
        try:
            page = hp.getHtml(currenturl)
        except urllib.error.URLError:
            continue

        url = regex.get_text('<a\shref="(\S+?)"><h3\sclass="title"',page)
        date = regex.get_text('<span\sclass="date">(\S+?\s\d+,\s\d+?)\s\S+\s\S+?\s\S+<\/span>',page)

        for cnt in range(0,len(date)):
            date[cnt] = fmt.convert_date(date[cnt])
            if date_ > date[cnt]:
                reach_updated = True
                break



        for i in range(0,cnt+1):
            try:
                urls['https://www.cbsnews.com' + url[i]] = str(date[i])[0:4]+'-'+str(date[i])[4:6] +'-'+str(date[i])[6:8]
            except IndexError:
                break




           
        if reach_updated:
            break

        index += 10
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

        title = regex.get_data('<title>([^<]+?)\s-\s[^<]+?<\/title>',html)
        if title == 'Noun':
            title = regex.get_data('<title>([^<]+?)<\/title>',html)
        author = regex.get_data('"author":{".type":"[^"]+?","name":"([^"]+?)"}',html)

        text1 = []
        text1.append(regex.get_data('<div\sdata-page=[^>]+?><[^>]*?>\n?([^\n]+?)<.?p>',html))
        text2 = regex.get_text('<p>([^\n]+?)<\/p>',html) 
        text = text1+text2

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
        data_print[url]['source'] = fmt.formatted_source("CBS")
        # line 5
        data_print[url]['url'] = fmt.formatted_url(url)
        # line 6
        data_print[url]['date'] = fmt.formatted_date(urls[url])
        # line 7
        if len(author) != 0:
            aa = author.split(',')
            if len(aa) > 1:
                author = ','.join(aa[:-1])
            elif len(aa) == 0:
                author = 'Noun Noun'
        else:
            author = 'Noun Noun'

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
    cbs(data_base,data_print,'health%20reform',0)   
    import output_file
    output_file.output(data_base)