import requests
import csv
import numpy as np
import pandas as pd
import os

def init():
    if not os.path.exists('./navData.csv'):
        with open('./navData.csv', 'w',encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'typeName',
                'gid',
                'containerid'
            ])


def writerRow(row):
    with open('./navData.csv', 'a', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)

def get_data(url):
    headers = {
        'Cookie': 'SUB=_2AkMS5U-Ff8NxqwFRmfoQym_qbolxwgvEieKkub5eJRMxHRl-yT9kqnYgtRB6OWVhah-VYmHrtZxBftHiXTkSebnzcSwi; XSRF-TOKEN=JiDJBwbIExFLRsqohO2-CdNH; WBPSESS=V0zdZ7jH8_6F0CA8c_ussbd_sbfr34c9_1AGLGD7lWf0V_vPso-CHuVHVL60mBF3VZnNSb5sFK8W9BQpd8XFpCgPX98jo2yPBZyJ3rggIObCWW09ghM2gyzNYkhY8WaxLDbd8LgmQ03tJD_yoI4_TnRr1LGBkp-cBNZymOeyMts=',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.3.5211 SLBChan/109'
    }

    params={
        'is_new_segment':1,
        'fetch_hot':1
      }
    response = requests.get(url, headers=headers, params=params,verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def parse_json(response):
    navList=np.append(response['groups'][3]['group'],response['groups'][4]['group'])
    for nav in navList:
         navName=nav['title']
         gid=nav['gid']
         containerid=nav['containerid']
         writerRow([navName,
               gid,
               containerid
               ])

if __name__ == '__main__':
    init()
    url='https://weibo.com/ajax/feed/allGroups'
    response=get_data(url)
    parse_json(response)
