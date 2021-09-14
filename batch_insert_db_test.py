import sys
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

# 테이블 생성 - MASTER (데이터 타입은 TEST, NUMERIC, INTEGER, REAL, BLOB 등)
db.execute("CREATE TABLE IF NOT EXISTS SNS_TWITTER_MASTER \
     (ID TEXT, CREATE_AT TEXT, USER_NAME TEXT, USER_SCREEN_NAME TEXT, TEXT TEXT, FAVORITE_COUNT INTEGER, RETWEET_COUNT INTEGER, HASHTAGS TEXT, SEARCH_QUERY TEXT, REMARK TEXT, PRIMARY KEY(ID))")

# 테이블 생성 - DEETAIL
db.execute("CREATE TABLE IF NOT EXISTS SNS_TWITTER_DETAIL \
     (ID TEXT, COLLECT_AT TEXT, FAVORITE_COUNT INTEGER, RETWEET_COUNT INTEGER, SEARCH_QUERY TEXT, REMARK TEXT, PRIMARY KEY(ID, COLLECT_AT))")

# 테이블 생성 - ALL
db.execute("CREATE TABLE IF NOT EXISTS SNS_TWITTER_TOTAL \
     (COLLECT_AT TEXT, ID TEXT, CREATE_AT TEXT, USER_NAME TEXT, USER_SCREEN_NAME TEXT, TEXT TEXT, FAVORITE_COUNT INTEGER, RETWEET_COUNT INTEGER, HASHTAGS TEXT, SEARCH_QUERY TEXT, REMARK TEXT, PRIMARY KEY(COLLECT_AT, ID))")


# twitter_api = twitter.Api(consumer_key=secrets.TWITTER_CONSUMER_KEY,
#                             consumer_secret=secrets.TWITTER_CONSUMER_SECRET, 
#                             access_token_key=secrets.TWITTER_ACCESS_TOKEN, 
#                             access_token_secret=secrets.TWITTER_ACCESS_SECRET)

# 키워드로 검색하기
keyword = '에피민트 OR #에피민트 AND exclude:retweets'
# # keyword = '#에피민트'
# statuses = twitter_api.GetSearch(term=keyword, count=100, result_type="recent", return_json=False)
# statuses_json = twitter_api.GetSearch(term=keyword, count=100, result_type="recent", return_json=True)

# for status in statuses:

#     # 트윗일시
#     create_at = datetime.strptime(status.created_at,'%a %b %d %H:%M:%S +0000 %Y') + timedelta(hours=9)
#     # 트윗일자
#     create_at_date = create_at.strftime('%Y-%m-%d')
    
#     print('create_at : ' + str(create_at))
#     print('id_str : ' + status.id_str)
#     print('name : ' + status.user.name)
#     print('screen_name : ' + status.user.screen_name)
#     print('favorite_count : ' + str(status.favorite_count))
#     print('retweet_count : ' + str(status.retweet_count))
#     print('text : ' + status.text)
#     print('--------------------------------------------------')

# print(f"검색어 '{keyword}'로 검색된 건수 : {len(statuses)}건")

file_name = '210910112840'
# file_name = '210913153640'
# file_name = '210913153747'

outfile = open(common.resource_path('history\{}.json').format(file_name, 'r'))
statuses_json = json.load(outfile)

# # print(len(statuses))
# # print(json.dumps(statuses_json, indent="\t"))
# print(len(statuses_json['statuses']))

commit_master_count = 0
commit_detail_count = 0

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
        db.execute("INSERT INTO SNS_TWITTER_TOTAL(COLLECT_AT, ID, CREATE_AT, USER_NAME, USER_SCREEN_NAME, TEXT, FAVORITE_COUNT, RETWEET_COUNT, HASHTAGS, SEARCH_QUERY, REMARK) \
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", \
                ( datetime.strptime('20{}'.format(file_name),'%Y%m%d%H%M%S')
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
        print('master 삽입 오류')
        # print('SQLite error: %s' % (' '.join(er.args)))
        # print("Exception class is: ", er.__class__)
        # print('SQLite traceback: ')
        # exc_type, exc_value, exc_tb = sys.exc_info()
        # print(traceback.format_exception(exc_type, exc_value, exc_tb))

    # region 마스터 - 디테일

    # # 데이터 조회 - Master
    # db.execute("SELECT ID FROM SNS_TWITTER_MASTER WHERE ID=:P_ID", {"P_ID": status['id_str']})
    # # print('fetchall', db.fetchall())

    # master_retreive_data = db.fetchall()
    # print('master - retreive_data', master_retreive_data)
    # print('master - retreive_data count', len(master_retreive_data))

    # # 데이터 조회 - Deteail
    # db.execute("SELECT ID FROM SNS_TWITTER_DETAIL WHERE ID=:P_ID AND COLLECT_AT=:P_COLLECT_AT", {"P_ID": status['id_str'], "P_COLLECT_AT": datetime.strptime('20{}'.format(file_name),'%Y%m%d%H%M%S')})
    # detail_retreive_data = db.fetchall()
    # print('detail - retreive_data', detail_retreive_data)
    # print('detail - retreive_data count', len(detail_retreive_data))

    # # if len(master_retreive_data) == 0:
    # #     print('insert - master')
    # try:
    #     # 데이터 삽입
    #     db.execute("INSERT INTO SNS_TWITTER_MASTER(ID, CREATE_AT, USER_NAME, USER_SCREEN_NAME, TEXT, FAVORITE_COUNT, RETWEET_COUNT, HASHTAGS, SEARCH_QUERY, REMARK) \
    #         VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", \
    #             (status['id_str']
    #             , datetime.strptime(status['created_at'],'%a %b %d %H:%M:%S +0000 %Y') + timedelta(hours=9)
    #             , status['user']['name']
    #             , status['user']['screen_name']
    #             , status['text']
    #             , status['favorite_count']
    #             , status['retweet_count']
    #             , ', '.join(map(str, [ h['text'] for h in status['entities']['hashtags'] if 'hashtags' in status['entities']]))
    #             , keyword
    #             , None
    #             ))

    #     commit_master_count += 1
    # except sqlite3.Error as er:
    #     print('master 삽입 오류')
    #     # print('SQLite error: %s' % (' '.join(er.args)))
    #     # print("Exception class is: ", er.__class__)
    #     # print('SQLite traceback: ')
    #     # exc_type, exc_value, exc_tb = sys.exc_info()
    #     # print(traceback.format_exception(exc_type, exc_value, exc_tb))

    #     # 디테일 삽입
    #     try:
    #         # 데이터 삽입
    #         db.execute("INSERT INTO SNS_TWITTER_DETAIL(ID, COLLECT_AT, FAVORITE_COUNT, RETWEET_COUNT, SEARCH_QUERY, REMARK) \
    #             VALUES(?, ?, ?, ?, ?, ?)", \
    #                 (status['id_str']
    #                 , datetime.strptime('20{}'.format(file_name),'%Y%m%d%H%M%S')
    #                 , status['favorite_count']
    #                 , status['retweet_count']
    #                 , keyword
    #                 , None
    #                 ))

    #         commit_detail_count += 1
    #     except sqlite3.Error as er:
    #         print('detail 삽입 오류')
    #         print('SQLite error: %s' % (' '.join(er.args)))
    #         print("Exception class is: ", er.__class__)
    #         print('SQLite traceback: ')
    #         exc_type, exc_value, exc_tb = sys.exc_info()
    #         print(traceback.format_exception(exc_type, exc_value, exc_tb))
    # # else:
    # #     print('insert - detail')
    # #     try:
    # #         # 데이터 삽입
    # #         db.execute("INSERT INTO SNS_TWITTER_DETAIL(ID, COLLECT_AT, FAVORITE_COUNT, RETWEET_COUNT, SEARCH_QUERY, REMARK) \
    # #             VALUES(?, ?, ?, ?, ?, ?)", \
    # #                 (status['id_str']
    # #                 , datetime.strptime('20{}'.format(file_name),'%Y%m%d%H%M%S')
    # #                 , status['favorite_count']
    # #                 , status['retweet_count']
    # #                 , keyword
    # #                 , None
    # #                 ))

    # #         commit_detail_count += 1
    # #     except sqlite3.Error as er:

    # #         print('SQLite error: %s' % (' '.join(er.args)))
    # #         print("Exception class is: ", er.__class__)
    # #         print('SQLite traceback: ')
    # #         exc_type, exc_value, exc_tb = sys.exc_info()
    # #         print(traceback.format_exception(exc_type, exc_value, exc_tb))
        
    # endregion

db.close()
print(commit_master_count)
print(commit_detail_count)