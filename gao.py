# coding=utf-8

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
    js = json.loads(r.text)
    with open(tag+'.txt', 'a+') as f:
        book_list = js['books']
        if not book_list:
            print tag+' is completely downloaded !'
            global done
            done = True
            return
        for book in book_list:
            f.write(repr(book)+'\n')
    print 'Book from '+str(start)+' to '+str(start+count-1)+' is downloaded.'


def gao():
    lasti = 0
    for i in range(0, 150000, 100):
        if done:
            break
        if i-lasti >= 1000:
            t = random.randint(10, 40)
            print 'sleep for %ds' %t
            time.sleep(t)
            lasti = i
        get_books_by_tag('小说', i, 100)


if __name__ == '__main__':
    gao()
