#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

symbols = ['.',',','"',':','(',')',';','[',']','{','}','£','!','?','$','#','%','&',\
            '@','^','*','+','-','/','\\','<','>','“','”']

'''
def formatted_content_with_symbol(text):
    count_space = 0
    count_non_space = 0 
    line = ''
    if_space = False
    
    line += '<u> '
    for sentence in text:

        if len(sentence) < 10:
            continue 

        i = 0
        cont = False
        if_jump = False


        while i < len(sentence):
            i_save = i

            if sentence[i] == '<':
                for j in range(i, len(sentence)):
                    if sentence[j] == '>':
                        i = j+1
                        if j == len(sentence)-1:
                            cont = True
                        break

            if cont:
                continue

            if sentence[i] == '&':
                cccccount = 0
                for j in range(i, len(sentence)):
                    cccccount += 1
                    if sentence[j] == ';':
                        i = j+1
                        if j == len(sentence)-1:
                            cont = True
                        break
                    if cccccount > 8:
                        break;
            if cont:
                continue

            if if_space and sentence[i] == ' ':
                i +=1
                count_space += 1
                continue
            if sentence[i] == '\n':
                line += ' '
                count_space += 1
                i +=1
                continue

            if sentence[i] in symbols :
                if i < len(sentence)-1 and sentence[i_save-1].isdigit() and sentence[i+1].isdigit():
                    line += sentence[i]
                    count_non_space += 1
                elif i < len(sentence)-1 and sentence[i_save-1].isalpha() and sentence[i+1].isalpha():
                    line += sentence[i]
                    count_non_space += 1
                elif i < len(sentence)-1 and if_space and sentence[i+1] == ' ':
                    line += sentence[i]
                    count_non_space += 1
                elif if_space:
                    line += sentence[i]
                    line += ' '
                    count_non_space += 1
                elif not if_space:
                    line += ' '
                    line += sentence[i]
                    count_non_space += 1

                i += 1
                continue

            if sentence[i] == ' ':
                if_space = True
                line += sentence[i]
                count_space += 1
            else:
                if_space = False
                line += sentence[i]
                count_non_space += 1

            i += 1

        
        if count_non_space > count_space and len(sentence) > 5:
            if len(sentence) != 0 and sentence[len(sentence)-1] == ' ':
                line += '<br> '
            else:
                line += ' <br> '

    if line[len(line)-1] == ' ':
        line += '</u>\n'
    else:
        line += ' </u>\n'

    line = re.sub(r'<br>\s+</u>', '</u> ', line)


    return line

def formatted_content(text):

    count_non_space = 0
    count_space = 0
    line = ''
    if_space = False

    line += '<a> '
    for sentence in text:

        if len(sentence) < 10:
                continue 

        i = 0
        cont = False
        #fix_sentence = []
        while i < len(sentence):

            
            if sentence[i] == '<':
                for j in range(i, len(sentence)):
                    if sentence[j] == '>':
                        i = j+1
                        if j == len(sentence)-1:
                            cont = True
                        break

            if cont:
                continue

            if sentence[i] == '&':
                cccccount = 0
                for j in range(i, len(sentence)):
                    cccccount += 1
                    if sentence[j] == ';':
                        i = j+1
                        if j == len(sentence)-1:
                            cont = True
                        break
                    if cccccount > 8:
                        break;
            if cont:
                continue


            if if_space and sentence[i] == ' ':
                i +=1
                count_space += 1
                continue
            if sentence[i] == '\n':
                line += ' '
                i +=1
                continue
            #fix_sentence += sentence[i]
            if sentence[i] == ' ':
                if_space = True
                line += sentence[i]
                count_space += 1
            else:
                if_space = False
                line += sentence[i]
                count_non_space += 1
            i += 1
        
        if count_non_space > count_space and len(sentence) > 5:
            if len(sentence) > 8 and sentence[len(sentence)-1] == ' ':
                line += '<br> '
            else:
                line += ' <br> '
        #new_text.append(fix_sentence)

    if line[len(line)-1] == ' ':
        line += '</a>\n'
    else:
        line += ' </a>\n'

    line = re.sub(r'<br>\s+</a>', '</a> ', line)

    return line
'''


def formatted_content(text):
    line = ''
    for sentence in text:
        sentence = re.sub(r'<[^>]*?>', '', sentence)
        sentence = re.sub(r'&[^;]*?;', '', sentence)
        sentence = re.sub(r'\n', ' ', sentence)
        sentence = re.sub(r'[ ]+;', ' ', sentence)

        if len(sentence) < 10:
            continue

        line += sentence
        line += ' <br> '

    line = line[:-6]
    line = re.sub(r'\s+', ' ', line)
    line += '\n'
    
    return line

def formatted_id(id_):
    #return "<id> " +str(id_)+ " </id>\n"
    return str(id_)+ "\n"

def formatted_key(key):
    #return "<key> " +key+ " </key>\n"
    return key+"\n"


def formatted_title(title):
    line = ''
    #line += "<title> "
    try:
        line += re.sub(r'&\S+?;', '',title)
    except IndexError:
        line += "None"
    #line += " </title>\n"
    line += "\n"

    return line


def formatted_source(source):
    #return "<source> " +source+ " </source>\n"
    return source+ "\n"

def formatted_url(url):
    #return "<url> " +url+ " </url>\n"
    return url+ "\n"

def formatted_date(date):
    line = ''
    #line += "<date> "
    if len(date) != 0:
        line += date
    else:
        line += "None"
    #line += " </date>\n"
    line += "\n"

    return line


def formatted_author(author,symbol):
    line = ''
    #if author == [] or author[0] == '':
    #    line += '<n> None Noue </n>\n'
    #else:
    #line += '<n> '
    author = author.split(symbol)
    line += author[0]
    for i in range(1,len(author)):
        #line += ' </n> <n> '
        line += ' and '
        line += author[i]
    #line += ' </n>\n'
    line += '\n'

    return line

def file_name(key, symbol):
    key2 = key.split("%20")
    kkey = ''
    for i in key2:
        kkey += i
        kkey += symbol
    return kkey[:-1]

def convert_date(date):
    if len(date) == 12:
        if date[0:3] == 'Jan':
            return int(date[8:12]+'01'+date[4:6])
        elif date[0:3] == 'Feb':
            return int(date[8:12]+'02'+date[4:6])
        elif date[0:3] == 'Mar':
            return int(date[8:12]+'03'+date[4:6])
        elif date[0:3] == 'Apr':
            return int(date[8:12]+'04'+date[4:6])
        elif date[0:3] == 'May':
            return int(date[8:12]+'05'+date[4:6])
        elif date[0:3] == 'Jun':
            return int(date[8:12]+'06'+date[4:6])
        elif date[0:3] == 'Jul':
            return int(date[8:12]+'07'+date[4:6])
        elif date[0:3] == 'Aug':
            return int(date[8:12]+'08'+date[4:6])
        elif date[0:3] == 'Sep':
            return int(date[8:12]+'09'+date[4:6])
        elif date[0:3] == 'Oct':
            return int(date[8:12]+'10'+date[4:6])
        elif date[0:3] == 'Nov':
            return int(date[8:12]+'11'+date[4:6])
        elif date[0:3] == 'Dec':
            return int(date[8:12]+'12'+date[4:6])
    else:
        if date[0:3] == 'Jan':
            return int(date[7:11]+'010'+date[4])
        elif date[0:3] == 'Feb':
            return int(date[7:11]+'020'+date[4])
        elif date[0:3] == 'Mar':
            return int(date[7:11]+'030'+date[4])
        elif date[0:3] == 'Apr':
            return int(date[7:11]+'040'+date[4])
        elif date[0:3] == 'May':
            return int(date[7:11]+'050'+date[4])
        elif date[0:3] == 'Jun':
            return int(date[7:11]+'060'+date[4])
        elif date[0:3] == 'Jul':
            return int(date[7:11]+'070'+date[4])
        elif date[0:3] == 'Aug':
            return int(date[7:11]+'080'+date[4])
        elif date[0:3] == 'Sep':
            return int(date[7:11]+'090'+date[4])
        elif date[0:3] == 'Oct':
            return int(date[7:11]+'100'+date[4])
        elif date[0:3] == 'Nov':
            return int(date[7:11]+'110'+date[4])
        elif date[0:3] == 'Dec':
            return int(date[7:11]+'120'+date[4])
