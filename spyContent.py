import re
import time
from datetime import datetime

import requests
import csv
import numpy as np
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

def init():
    if not os.path.exists('../model/navArticle.csv'):
        with open('../model/navArticle.csv', 'w', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'id',
                'likeNum',
                'commentsLen',
                'reposts_count',
                'region',
                'content',
                'contentLen',
                'created_at',
                'type',
                'detailUrl',
                'authorAvatar',
                'authorName',
                'authorDetail',
                'isVip'
            ])


def writerRow(row):
    with open('./navArticle.csv', 'a', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)

def get_data(url,params):
    headers={
        'Cookie':'SUB=_2AkMS5U-Ff8NxqwFRmfoQym_qbolxwgvEieKkub5eJRMxHRl-yT9kqnYgtRB6OWVhah-VYmHrtZxBftHiXTkSebnzcSwi; XSRF-TOKEN=JiDJBwbIExFLRsqohO2-CdNH; WBPSESS=V0zdZ7jH8_6F0CA8c_ussbd_sbfr34c9_1AGLGD7lWf0V_vPso-CHuVHVL60mBF3VZnNSb5sFK8W9BQpd8XFpCgPX98jo2yPBZyJ3rggIObCWW09ghM2gyzNYkhY8WaxLDbd8LgmQ03tJD_yoI4_TnRr1LGBkp-cBNZymOeyMts=',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.3.5211 SLBChan/109'
    }

    response = requests.get(url, headers=headers, params=params,verify=False)
    if response.status_code == 200:
        return response.json()['statuses']
    else:
        return None

def getAllTypeList():
    typeList=[]
    with open('./navData2.csv', 'r', encoding='utf-8') as reader:
        readerCsv=csv.reader(reader)
        next(reader)
        for nav in readerCsv:
            if len(nav)==0:continue
            typeList.append(nav)

    return typeList

def parse_json(response,type):
    for article in response:
        id=article['id']
        likeNum=article['attitudes_count']
        commentsLen=article['comments_count']
        reposts_count=article['reposts_count']

        try:
            region=article['region_name'].replace('发布于 ','')
        except:
            region='无'
        content=article['text_raw']
        try:
            contentLen=article['textLength']
        except:
            contentLen=0
        created_at=datetime.strptime(article['created_at'],'%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d')
        type=type
        try:
             detailUrl='https://weibo.com/'+article['idstr']+'/'+str(article['mblogid'])
        except:
             detailUrl='无'
        authorAvatar=article['user']['avatar_large']
        authorName=article['user']['screen_name']
        authorDetail='https://weibo.com/u/'+str(article['user']['id'])
        if article['user']['v_plus']:
            isVip = article['user']['v_plus']
        else:
            isVip = 0

        # 去掉括号和标点符号的函数
        def clean_text(text):
            return re.sub(r'[(){}，。！？；：“”‘’]', '', text)
        # 写入的时候处理数据
        writerRow([
            clean_text(str(id)),
            clean_text(str(likeNum)),
            clean_text(str(commentsLen)),
            clean_text(str(reposts_count)),
            clean_text(region),
            clean_text(content),
            clean_text(str(contentLen)),
            clean_text(created_at),
            clean_text(type),
            clean_text(detailUrl),
            clean_text(authorAvatar),
            clean_text(authorName),
            clean_text(authorDetail),
            clean_text(str(isVip))
        ])


def start(typeNum=3,pageNum=2):
    articleUrl='https://weibo.com/ajax/feed/hottimeline'
    init()
    typeList=getAllTypeList()
    typeNumCount=0
    for type in typeList:
        if typeNumCount>=typeNum:return
        time.sleep(0.5)
        for page in range(0,pageNum):
            time.sleep(0.5)
            print('正在爬取的类型 %s 中的第%s页文章数据' %(type[0],page+1))
            params={
                'group_id':type[1],
                'containerid':type[2],
                'max_id':page,
                'count':10,
                'extparam':'discover|new_feed'
            }
            response=get_data(articleUrl,params)
            parse_json(response,type[0])
        typeNumCount+=1

if __name__ == '__main__':
    start()


