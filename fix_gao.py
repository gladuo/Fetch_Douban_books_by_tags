# coding=utf-8

import os
import ast
import codecs
import json
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

API_SEARCH_URL = 'https://api.douban.com/v2/book/search'


def fix_gao_test():
    payload = {
        'tag': '安妮宝贝',
        'start': 0,
        'count': 5,
    }
    r = requests.get(API_SEARCH_URL, payload)
    # print r.headers
    js = json.loads(r.text)
    print json.dumps(js['books'][0], ensure_ascii=False)


def fix_gao():
    curpath = os.path.abspath('./')
    for text in os.listdir(curpath):
        file_path = os.path.join(curpath, text)
        if file_path is not os.path.isdir:
            if os.path.splitext(file_path)[1] == '.txt':
                print file_path
                with open(file_path, 'r') as fr:
                    json_path = os.path.join(curpath, os.path.splitext(file_path)[0]+'.json')
                    if os.path.exists(json_path):
                        continue
                    with open(json_path, 'w') as fw:
                        for line in fr.readlines():
                            # print json.dumps(ast.literal_eval(line), ensure_ascii=False)
                            try:
                                fw.write(json.dumps(ast.literal_eval(line), ensure_ascii=False)+'\n')
                            except SyntaxError:
                                print '---------------'
                                print file_path
                                print line
                                print '---------------'
                                continue


if __name__ == '__main__':
    fix_gao()
