import time
from datetime import datetime

import requests
import csv
import numpy as np
import pandas as pd
import os

def init():
    if not os.path.exists('../model/articleComment.csv'):
        with open('../model/articleComment.csv', 'w', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'articleId',
                'created_at',
                'likes_counts',
                'region',
                'content',
                'authorName',
                'authorGender',
                'authorAddress',
                'authorAvatar'
            ])


def writerRow(row):
    with open('../model/articleComment.csv', 'a', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)

def get_data(url,params):
    headers = {
        'Cookie': 'SUB=_2AkMS5U-Ff8NxqwFRmfoQym_qbolxwgvEieKkub5eJRMxHRl-yT9kqnYgtRB6OWVhah-VYmHrtZxBftHiXTkSebnzcSwi; XSRF-TOKEN=JiDJBwbIExFLRsqohO2-CdNH; WBPSESS=V0zdZ7jH8_6F0CA8c_ussbd_sbfr34c9_1AGLGD7lWf0V_vPso-CHuVHVL60mBF3VZnNSb5sFK8W9BQpd8XFpCgPX98jo2yPBZyJ3rggIObCWW09ghM2gyzNYkhY8WaxLDbd8LgmQ03tJD_yoI4_TnRr1LGBkp-cBNZymOeyMts=',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.3.5211 SLBChan/109'
    }

    response = requests.get(url, headers=headers, params=params,verify=False)
    if response.status_code == 200:
        return response.json()['data']
    else:
        return None

def getAllArticleList():
    typeList=[]
    with open('../model/navArticle.csv', 'r', encoding='utf-8') as reader:
        readerCsv=csv.reader(reader)
        next(reader)
        for nav in readerCsv:
            nav = [item.replace('(', '').replace(')', '').replace(',', '').strip() for item in nav]
            if len(nav)==0:continue
            typeList.append(nav)

    return typeList

def parse_json(response,articleId):
    for comment in response:
        created_at=datetime.strptime(comment['created_at'],'%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d')
        likes_counts=comment['like_counts']
        try:
            region = comment['source'].replace('来自', '')
        except:
            region='无'
        content=comment['text_raw']
        authorName=comment['user']['screen_name']
        authorGender=comment['user']['gender']
        authorAddress=comment['user']['location']
        authorAvatar=comment['user']['avatar_large']
        writerRow([
            articleId,
            created_at,
            likes_counts,
            region,
            content,
            authorName,
            authorGender,
            authorAddress,
            authorAvatar
        ])

def start():
    articleUrl = 'https://weibo.com/ajax/statuses/buildComments'
    init()
    articleList = getAllArticleList()
    for article in articleList:
        articleId = article[0]
        print('正在爬取id值为%s的文章' % articleId)
        time.sleep(1)
        params={
            'id':int(articleId),
            'is_show_bulletin':2
        }
        response = get_data(articleUrl,params)
        parse_json(response,articleId)


if __name__ == '__main__':
    start()


