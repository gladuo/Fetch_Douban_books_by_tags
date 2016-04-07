# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from pyquery import PyQuery as pq
import requests
import json
import time
import random

TAGS_URL = 'https://book.douban.com/tag/?view=type&icn=index-sorttags-hot'
API_SEARCH_URL = 'https://api.douban.com/v2/book/search'

done = False


def fetch_tags():
    d = pq(TAGS_URL)
    s = d('td').text()
    tag_list = s.split(' ')[2:]
    for tag in tag_list:
        print tag


def get_books_by_tag(tag='小说', start=0, count=100):
    payload = {
        'tag': tag,
        'start': start,
        'count': count,
    }
    r = requests.get(API_SEARCH_URL, payload)
    # print r.headers
    js = json.loads(r.text)
    with open(tag+'.json', 'a+') as f:
        book_list = js['books']
        if not book_list:
            print '--- %s is completely downloaded ! ---' % tag
            global done
            done = True
            return
        for book in book_list:
            f.write(json.dumps(book, ensure_ascii=False)+'\n')
    print '%s book from ' % tag+str(start)+' to '+str(start+count-1)+' is downloaded.'


def gao(tag='小说'):
    last_i = 0
    for i in range(0, 150000, 100):
        if done:
            break
        if i - last_i >= 1500:
            t = random.randint(10, 40)
            print 'sleep for %ds' % t
            time.sleep(t)
            last_i = i
        get_books_by_tag(tag, i, 100)


def get_books_by_tags():
    tags = []
    with open('tags.txt', 'r') as f:
        for tag in f.readlines():
            tags.append(tag.strip('\n'))

    for tag in tags:
        global done
        done = False
        print '--- %s is downloading ---' % tag
        gao(tag)
        print '--- %s is completely downloaded ! ---' % tag


if __name__ == '__main__':
    get_books_by_tags()
    # fetch_tags()
    # gao('科普')
