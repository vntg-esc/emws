import sys
import os
from datetime import datetime, timedelta
import json
import logging

# python-twitter
import twitter
from twitter import Status
# API KEY
import secrets
# 상수
import constant

# 공통 모듈
import common

### 파이썬 SQlite 라이브러리 블러오기 및 버전 확인
import sqlite3
import traceback

# print(sqlite3.version)
# print(sqlite3.sqlite_version)

### db연결, 커서 획득
# DB 생성 (오토 커밋)
conn = sqlite3.connect("emws_test.db", isolation_level=None)

# 커서 획득
db = conn.cursor()

# 테이블 생성 - ALL
db.execute("CREATE TABLE IF NOT EXISTS SNS_EPIMINT \
     (CAMPAIGN, COLLECT_AT TEXT, ID TEXT, CREATE_AT TEXT, USER_NAME TEXT, USER_SCREEN_NAME TEXT, TEXT TEXT, FAVORITE_COUNT INTEGER, RETWEET_COUNT INTEGER, HASHTAGS TEXT, SEARCH_QUERY TEXT, REMARK TEXT, PRIMARY KEY(CAMPAIGN, COLLECT_AT, ID))")

# 캠페인
campaign = 'twitter'
# 키워드로 검색하기
keyword = '에피민트 OR #에피민트 AND exclude:retweets'


path = "test/history/"
file_list = os.listdir('./' + path)

for file_name in file_list:
    if file_name[8:10] == '00':
        # print('file_name', file_name)
        outfile = open(common.resource_path('{}{}').format(path, file_name), 'r')
        statuses_json = json.load(outfile)

        file_name = file_name.replace('.json', '')
        # print('chg file_name', file_name)

        # # print(len(statuses))
        # # print(json.dumps(statuses_json, indent="\t"))
        # print(len(statuses_json['statuses']))

        commit_master_count = 0

        for status in statuses_json['statuses']:
            # print('----------')
            # print(status['id_str'])
            # print(datetime.strptime(status['created_at'],'%a %b %d %H:%M:%S +0000 %Y') + timedelta(hours=9))
            # print(status['user']['name'])
            # print(status['user']['screen_name'])
            # print(status['text'])
            # print(status['favorite_count'])
            # print(status['retweet_count'])

        #     # list = [ h['text'] for h in status['entities']['hashtags'] if 'hashtags' in status['entities']]
        #     # listtostr = ' '.join(map(str, list))
        #     # print(listtostr)

        #     print(', '.join(map(str, [ h['text'] for h in status['entities']['hashtags'] if 'hashtags' in status['entities']])))
        #     print(keyword)

            try:
                # 데이터 삽입
                db.execute("INSERT INTO SNS_EPIMINT(CAMPAIGN, COLLECT_AT, ID, CREATE_AT, USER_NAME, USER_SCREEN_NAME, TEXT, FAVORITE_COUNT, RETWEET_COUNT, HASHTAGS, SEARCH_QUERY, REMARK) \
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", \
                        ( campaign
                        , datetime.strptime('20{}'.format(file_name),'%Y%m%d%H%M%S')
                        , status['id_str']
                        , datetime.strptime(status['created_at'],'%a %b %d %H:%M:%S +0000 %Y') + timedelta(hours=9)
                        , status['user']['name']
                        , status['user']['screen_name']
                        , status['text']
                        , status['favorite_count']
                        , status['retweet_count']
                        , ', '.join(map(str, [ h['text'] for h in status['entities']['hashtags'] if 'hashtags' in status['entities']]))
                        , keyword
                        , None
                        ))

                commit_master_count += 1
            except sqlite3.Error as er:
                
                print('SQLite error: %s' % (' '.join(er.args)))
                print("Exception class is: ", er.__class__)
                print('SQLite traceback: ')
                exc_type, exc_value, exc_tb = sys.exc_info()
                print(traceback.format_exception(exc_type, exc_value, exc_tb))

db.close()
print(commit_master_count)