import sys
import twitter
import datetime

def connTwitterAPI():
    # twitter_consumer_key = I"qbhQ1AwYrTFEMvxEnIMQcphA"
    # twitter_consumer_secret = k"2zx7wvF610rToWkkwkxDFNNHWuLLhTHDcnDoludDREh74H3jz"
    # twitter_access_token = q"153372335-p54Axs900ndAJKWm4cMQEytisgLWWKNJ7i4StYs"
    # twitter_access_secret = J"0DjinX48QlJ9yFz2MaR2KvN1i0pZJU7tNQOo4LfdoDyK"

    # twitter api 연동시작
    # twitter_api = twitter.Api()
    twitter_api = twitter.Api(consumer_key=twitter_consumer_key,
                            consumer_secret=twitter_consumer_secret, 
                            access_token_key=twitter_access_token, 
                            access_token_secret=twitter_access_secret)

    return twitter_api

def getSearchTwittbyKeyword(twitter_api, query):

    statuses = twitter_api.GetSearch(term=query, count=3)
    return statuses

def main(keyword):
    # 키워드로 검색하기
    statuses = getSearchTwittbyKeyword(connTwitterAPI(), keyword)

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
    """
    Author : 현이
    Content : 트위터에서 검색어를 이용한 트윗 게시물 건수, 좋아요 수, 리트윗 수 추출
    Data: 2021.08.18
    Useage: main.py '검색어'
    """
    # 파라미터가 있는지 확인 - 없으면 기본 : '에피민트'
    if len(sys.argv) == 1:
        sys.argv.append('에피민트')

    # main 실행
    main(sys.argv[1])