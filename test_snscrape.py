# pip install snscrape
# pip install pandas
import pandas as pd
import string
import re
import warnings
import snscrape.modules.twitter as sntwitter
from time import sleep
import datetime

warnings.filterwarnings(action='ignore')

def read_tweet_list(twitterName, startDay, endDay):
    tweets_list1 = []
    tweets_df2 = pd.DataFrame(columns=['URL', 'Datetime', 'Tweet Id', 'Content', 'Username'])

    if pd.isnull(twitterName) or twitterName == "":
        return tweets_df2

    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(
            'from:' + twitterName + ' since:' + startDay + ' until:' + endDay + '').get_items()):
        tweets_list1.append([tweet.url, tweet.date, tweet.id, tweet.content.encode('utf-8'), tweet.username])
        tweets_df2 = pd.DataFrame(tweets_list1, columns=['URL', 'Datetime', 'Tweet Id', 'Content', 'Username'])

    return tweets_df2


st_day = '2020-01-01'
ed_day = '2021-07-23'

log_file_path = './log.txt'

target_tweet_name = ['elonmusk']

for sid in target_tweet_name:
    print(f'{sid} 크롤링 시작')
    try:
        if pd.isnull(sid) or sid == '':
            with open(log_file_path, 'a') as file:
                file.write('잘못된 닉네임입니다. 로그 저장 시각 : ' + str(datetime.datetime.now()) + "\n")
            file.close()
            continue
        result = read_tweet_list(sid, st_day, ed_day)
        result.to_csv(f'./out/{sid}_out_{st_day}_{ed_day}.csv', index=False, header=True)
        print('크롤링 성공, 데이터 총 량 : ', len(result))
        with open(log_file_path, 'a') as file:
            file.write(sid + ' 아이디의 트위터 검색 완료! 총 ' + str(len(result)) + '개의 트위터를 찾았습니다. 로그 저장 시각 : ' + str(
                datetime.datetime.now()) + "\n")
        file.close()
    except Exception as e:
        print(f'{sid} 오류 발생')
        with open(log_file_path, 'a') as file:
            file.write(sid + ' 아이디의 트위터의 검색 중 ' + str(e) + ' 오류가 발생했습니다. 해당 아이디를 건너뜁니다. 로그 저장 시각 : ' + str(
                datetime.datetime.now()) + "\n")
        file.close()
        continue
