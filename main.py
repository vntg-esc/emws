import sys
import twitter
import datetime
# API KEY
import secrets

def getSearchTwittbyKeyword(twitter_api, query):
    # 검색하기
    statuses = twitter_api.GetSearch(term=query, count=3)
    return statuses

def main(keyword):
    # twitter api 연동시작
    # twitter_api = twitter.Api()
    twitter_api = twitter.Api(consumer_key=secrets.TWITTER_CONSUMER_KEY,
                            consumer_secret=secrets.TWITTER_CONSUMER_SECRET, 
                            access_token_key=secrets.TWITTER_ACCESS_TOKEN, 
                            access_token_secret=secrets.TWITTER_ACCESS_SECRET)

    # 키워드로 검색하기
    statuses = getSearchTwittbyKeyword(twitter_api, keyword)

    # 검색 내용 출력
    for status in statuses:
        # print(status)
        print(status.id_str)
        print(status.user.screen_name)
        print(status.hashtags)
        print(status.favorite_count)
        print(datetime.datetime.strptime(status.created_at,'%a %b %d %H:%M:%S +0000 %Y') + datetime.timedelta(hours=9))
        # print(status.text.encode('utf-8'))
        print(status.text)
        print('-----------')
    print("'{}'로 검색된 건수 : {}건".format(keyword, len(statuses)))


if __name__ == '__main__':

    # 파라미터가 있는지 확인 - 없으면 기본 : '에피민트'
    if len(sys.argv) == 1:
        sys.argv.append('에피민트')

    # main 실행
    main(sys.argv[1])