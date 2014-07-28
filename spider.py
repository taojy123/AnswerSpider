#coding=utf8

import cookielib
import urllib2, urllib
import time
import re
import traceback
import time
import shutil
import hashlib
import json
import pprint
from models import *
from BeautifulSoup import BeautifulSoup


cj = cookielib.CookieJar()
#opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), urllib2.ProxyHandler({'http':"10.239.120.37:911"}))
opener.addheaders = [
                    ('User-agent', 'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1'),
                     ]

def get_page(url, data=None):
    resp = None
    n = 0
    while n < 3:
        n = n + 1
        try:
            resp = opener.open(url, data, timeout=5)
            page = resp.read()
            return page
        except:
            traceback.print_exc()
            time.sleep(2)
            print "Try after 2 seconds ..."
            continue
    raise Exception("Get page failed")



CN_URL = "http://irm.cninfo.com.cn/ircs/interaction/lastRepliesForSzse.do?pageNo=1"
SSE_URL = "http://sns.sseinfo.com/ajax/feeds.do?type=11&pageSize=30&lastid=-1&show=1&page=1"


def get_cn_data():
    print "Get CN"
    rs = []
    p = get_page(CN_URL)
    p = BeautifulSoup(p)
    boxs = p.findAll("div", {"class": "msgCnt gray666"})

    # p2 = get_page(CN_URL[:-1]+"2")
    # p2 = BeautifulSoup(p2)
    # boxs += p2.findAll("div", {"class": "msgCnt gray666"})

    # p3 = get_page(CN_URL[:-1]+"3")
    # p3 = BeautifulSoup(p3)
    # boxs += p3.findAll("div", {"class": "msgCnt gray666"})

    for i in range(len(boxs)-1, 0, -2):
        question = boxs[i-1]
        answer = boxs[i]
        alink = answer.find("a", {"class": "cntcolor"})
        question = question.getText()
        answer = answer.getText()
        url = "http://irm.cninfo.com.cn/ircs/interaction/" + alink.get("href")
        if not QA.gets(question=question, answer=answer):
            qa = QA()
            qa.origin = "CN"
            qa.question = question
            qa.answer = answer
            qa.url = url
            qa.save()
            rs.append(qa)
            print qa.id
    return rs


def get_sse_data():
    print "Get SSE"
    rs = []
    p = get_page(SSE_URL)
    p = BeautifulSoup(p)

    items = p.findAll("div", {"class": "m_feed_item"})
    items = items[::-1]

    for item in items:
        txts = item.findAll("div", {"class": "m_feed_txt"})
        question = txts[0]
        answer = txts[1]
        item_id = item.get("id")
        question = question.getText()
        answer = answer.getText()
        url = "http://sns.sseinfo.com/?" + item_id
        if not QA.gets(question=question, answer=answer):
            qa = QA()
            qa.origin = "SSE"
            qa.question = question
            qa.answer = answer
            qa.url = url
            qa.save()
            rs.append(qa)
            print qa.id
    return rs


if __name__ == "__main__":
    rs = get_cn_data()
    rs += get_sse_data()
    print rs






