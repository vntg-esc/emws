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

twitter_api = twitter.Api(consumer_key=secrets.TWITTER_CONSUMER_KEY,
                            consumer_secret=secrets.TWITTER_CONSUMER_SECRET, 
                            access_token_key=secrets.TWITTER_ACCESS_TOKEN, 
                            access_token_secret=secrets.TWITTER_ACCESS_SECRET)

# 키워드로 검색하기
# keyword = '#에피민트 AND exclude:retweets'
keyword = '#에피민트'
statuses = twitter_api.GetSearch(term=keyword, count=100, result_type="recent", return_json=False)

for status in statuses:

    # 트윗일시
    create_at = datetime.strptime(status.created_at,'%a %b %d %H:%M:%S +0000 %Y') + timedelta(hours=9)
    # 트윗일자
    create_at_date = create_at.strftime('%Y-%m-%d')
    
    print('create_at : ' + str(create_at))
    print('id_str : ' + status.id_str)
    print('name : ' + status.user.name)
    print('screen_name : ' + status.user.screen_name)
    print('favorite_count : ' + str(status.favorite_count))
    print('retweet_count : ' + str(status.retweet_count))
    print('text : ' + status.text)
    print('--------------------------------------------------')

print(f"검색어 '{keyword}'로 검색된 건수 : {len(statuses)}건")