import os, sys

data = open('data.txt', 'r')
url = open('url.txt', 'r')

article_count = 0

for x, y in zip(data, url):

    if x == '\n' or y == '\n':
        continue

    fw = open('Article_'+str(article_count), 'w')

    fw.write('#Unknown\n')
    fw.write(str(article_count)+'\n')
    fw.write(y)
    fw.write('tax reform\n')
    fw.write('#Summary\n')
    fw.write(x)
    article_count += 1
    fw.close()