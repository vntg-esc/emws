import sys
import twitter
import datetime
# API KEY
import secrets
# 필터 문자열
import constant

def getSearchTwittbyKeyword(twitter_api, query):
    # 검색하기
    statuses = twitter_api.GetSearch(term=query, count=100, result_type="recent")

    return statuses

    # # 검색하기 - 파일 저장
    # import json
    # statuses = twitter_api.GetSearch(term=query, count=100, result_type="recent", return_json=True)

    # with open("./sample.json", 'w') as outfile:
    #     json.dump(statuses, outfile)

def main(keyword):
    # twitter api 연동시작
    # twitter_api = twitter.Api()
    twitter_api = twitter.Api(consumer_key=secrets.TWITTER_CONSUMER_KEY,
                            consumer_secret=secrets.TWITTER_CONSUMER_SECRET, 
                            access_token_key=secrets.TWITTER_ACCESS_TOKEN, 
                            access_token_secret=secrets.TWITTER_ACCESS_SECRET)

    # 키워드로 검색하기
    statuses = getSearchTwittbyKeyword(twitter_api, keyword)

    # 일자별 트윗 정보 { '일자' : {'계정': {[게시글수, 좋아요수, 리트윗수]}}}
    twittDaysInfo = {}
    # 사용자별 트윗 정보
    # twittUserInfo = {}
    # 일자별 트윗 정보 상세 - 게시물수, 좋아요수
    # twittDetailInfo = {}

    # 검색 내용 출력
    for status in statuses:

        # 트윗일시
        create_at = datetime.datetime.strptime(status.created_at,'%a %b %d %H:%M:%S +0000 %Y') + datetime.timedelta(hours=9)
        # 트윗일자
        create_at_date = create_at.strftime('%Y-%m-%d')

        # 일자별 트윗 정보에 존재하는지 확인
        if create_at_date in twittDaysInfo:
            print('존재 : ' + create_at_date)

            # 조회된 정보 가져오기 및 누적
            twittUserInfo = twittDaysInfo.get(create_at_date)

            # 필터 문자열
            for filterStr in constant.C_FILTER_KEYWORD:
                # 사용자가 필터 문자열에 포함되는지 확인
                if filterStr in status.user.name:
                    # 사용자가 이미 저장되었는지 확인
                    if status.user.screen_name in twittUserInfo:
                        # 상세정보 - 트윗수, 좋아요수
                        twittDetailInfo = twittUserInfo.get(status.user.screen_name)

                        twittDetailInfo['writeCnt'] += 1
                        twittDetailInfo['likeCnt'] += status.favorite_count
                        twittDetailInfo['retwittCnt'] += status.retweet_count
                    else:
                        # 상세정보 - 트윗수, 좋아요수
                        twittDetailInfo = {
                                # 트윗수
                                'writeCnt': 1,
                                # 좋아요수
                                'likeCnt': status.favorite_count,
                                # 리트윗수
                                'retwittCnt': status.retweet_count
                        }
                        twittUserInfo[status.user.screen_name] = twittDetailInfo

                else:
                    if 'normal' in twittUserInfo:
                                                # 상세정보 - 트윗수, 좋아요수
                        # 상세정보 - 트윗수, 좋아요수
                        twittDetailInfo = twittUserInfo.get('normal')

                        twittDetailInfo['writeCnt'] += 1
                        twittDetailInfo['likeCnt'] = twittDetailInfo['likeCnt'] +  status.favorite_count
                        twittDetailInfo['retwittCnt'] = twittDetailInfo['retwittCnt'] +  status.retweet_count
                    else:
                        # 상세정보 - 트윗수, 좋아요수
                        twittDetailInfo = {
                                # 트윗수
                                'writeCnt': 1,
                                # 좋아요수
                                'likeCnt': status.favorite_count,
                                # 리트윗수
                                'retwittCnt': status.retweet_count
                        }
                        twittUserInfo['normal'] = twittDetailInfo

                # print('존재')
                # print('twittUserInfo')
                # print(twittUserInfo)
                # print('twittDaysInfo')
                # print(twittDaysInfo)
            
        else:
            print('미존재 : ' + create_at_date)
            
            # 필터 문자열
            for filterStr in constant.C_FILTER_KEYWORD:
                twittUserInfo = {}
                # 사용자가 필터 문자열에 포함되는지 확인
                if filterStr in status.user.name:
                    # 상세정보 - 트윗수, 좋아요수
                    twittDetailInfo = {
                                        # 트윗수
                                        'writeCnt': 1,
                                        # 좋아요수
                                        'likeCnt': status.favorite_count,
                                        # 리트윗수
                                        'retwittCnt': status.retweet_count
                                    }
                    # 일자별 사용자별 Dictionary
                    twittUserInfo[status.user.screen_name] = twittDetailInfo
                    # 일자별 상세정보 Dictionary
                    twittDaysInfo[create_at_date] = twittUserInfo
                else:
                    # 상세정보 - 트윗수, 좋아요수
                    twittDetailInfo = {
                                        # 트윗수
                                        'writeCnt': 1,
                                        # 좋아요수
                                        'likeCnt': status.favorite_count,
                                        # 리트윗수
                                        'retwittCnt': status.retweet_count
                                    }
                    # 일자별 사용자별 Dictionary
                    twittUserInfo['normal'] = twittDetailInfo
                    # 일자별 상세정보 Dictionary
                    twittDaysInfo[create_at_date] = twittUserInfo

                # print('미존재')
                # print('twittUserInfo')
                # print(twittUserInfo)
                # print('twittDaysInfo')
                # print(twittDaysInfo)

        # # 출력
        # print(status)
        print('id_str : ' + status.id_str)
        print('name : ' + status.user.name)
        print('screen_name : ' + status.user.screen_name)
        print('hashtags : ' + str(status.hashtags))
        print('favorite_count : ' + str(status.favorite_count))
        print('retweet_count : ' + str(status.retweet_count))
        print('create_at : ' + str(create_at))
        # print(status.text.encode('utf-8'))
        print('text : ' + status.text)
        print('-----------')

    print("'{}'로 검색된 건수 : {}건".format(keyword, len(statuses)))
    print(twittDaysInfo)


def main_test1(keyword):
    # twitter api 연동시작
    # twitter_api = twitter.Api()
    twitter_api = twitter.Api(consumer_key=secrets.TWITTER_CONSUMER_KEY,
                            consumer_secret=secrets.TWITTER_CONSUMER_SECRET, 
                            access_token_key=secrets.TWITTER_ACCESS_TOKEN, 
                            access_token_secret=secrets.TWITTER_ACCESS_SECRET)

    # 키워드로 검색하기
    statuses = getSearchTwittbyKeyword(twitter_api, keyword)

    # 일자별 트윗 정보 { '일자' : {[게시글수, 좋아요수, 리트윗수]}}
    twittDaysInfo = {}
    # 일자별 트윗 정보 상세 - 게시물수, 좋아요수
    # twittDetailInfo = {}

    # 검색 내용 출력
    for status in statuses:

        # 트윗일시
        create_at = datetime.datetime.strptime(status.created_at,'%a %b %d %H:%M:%S +0000 %Y') + datetime.timedelta(hours=9)
        # 트윗일자
        create_at_date = create_at.strftime('%Y-%m-%d')

        # 일자별 트윗 정보에 존재하는지 확인
        if create_at_date in twittDaysInfo:
            print('존재 : ' + create_at_date)

            # 조회된 정보 가져오기 및 누적
            twittDetailInfo = twittDaysInfo.get(create_at_date)

            twittDetailInfo['writeCnt'] += 1
            twittDetailInfo['likeCnt'] = twittDetailInfo['likeCnt'] +  status.favorite_count
            twittDetailInfo['retwittCnt'] = twittDetailInfo['retwittCnt'] +  status.retweet_count
            
        else:
            print('미존재 : ' + create_at_date)
            
            # 상세정보 - 트윗수, 좋아요수
            twittDetailInfo = {
                                # 트윗수
                                'writeCnt': 1,
                                # 좋아요수
                                'likeCnt': status.favorite_count,
                                # 리트윗수
                                'retwittCnt': status.retweet_count
                            }

            # 일자별 상세정보 Dictionary
            twittDaysInfo[create_at_date] = twittDetailInfo


        # # 출력
        # print(status)
        # print('id_str : ' + status.id_str)
        # print('name : ' + status.user.name)
        # print('screen_name : ' + status.user.screen_name)
        # print('hashtags : ' + str(status.hashtags))
        # print('favorite_count : ' + str(status.favorite_count))
        # print('retweet_count : ' + str(status.retweet_count))
        # print('create_at : ' + str(create_at))
        # # print(status.text.encode('utf-8'))
        # print('text : ' + status.text)
        # print('-----------')

    print("'{}'로 검색된 건수 : {}건".format(keyword, len(statuses)))
    print(twittDaysInfo)


if __name__ == '__main__':

    # 파라미터가 있는지 확인 - 없으면 기본 : '에피민트'
    if len(sys.argv) == 1:
        sys.argv.append('에피민트')

    # print()
    # print()
    # print()
    # print()
    # print()
    print('-----------')

    # main 실행
    main(sys.argv[1])
    # main_test1(sys.argv[1])

    
# {
#     '2021-08-30': {'writeCnt': 2, 'likeCnt': 6}, 
#     '2021-08-29': {'writeCnt': 4, 'likeCnt': 1}, 
#     '2021-08-28': {'writeCnt': 5, 'likeCnt': 10}, 
#     '2021-08-27': {'writeCnt': 2, 'likeCnt': 4}, 
#     '2021-08-26': {'writeCnt': 2, 'likeCnt': 3}, 
#     '2021-08-25': {'writeCnt': 4, 'likeCnt': 10}, 
#     '2021-08-24': {'writeCnt': 18, 'likeCnt': 33}, 
#     '2021-08-23': {'writeCnt': 6, 'likeCnt': 2}, 
#     '2021-08-22': {'writeCnt': 10, 'likeCnt': 11}
#     }

# {
#     '2021-08-30': {
#         'human': {'writeCnt': 6, 'likeCnt': 7, 'retwittCnt': 17},
#         'sell_coupons': {'writeCnt': 3, 'likeCnt': 0, 'retwittCnt': 713}},
#     '2021-08-29': {
#         'human': {'writeCnt': 6, 'likeCnt': 7, 'retwittCnt': 17}, 
#         'sell_coupons': {'writeCnt': 3, 'likeCnt': 0, 'retwittCnt': 713}}, 
#     '2021-08-28': {
#         'human': {'writeCnt': 6, 'likeCnt': 7, 'retwittCnt': 17}, 
#         'sell_coupons': {'writeCnt': 3, 'likeCnt': 0, 'retwittCnt': 713}}, 
#     '2021-08-27': {
#         'human': {'writeCnt': 6, 'likeCnt': 7, 'retwittCnt': 17},
#         'sell_coupons': {'writeCnt': 3, 'likeCnt': 0, 'retwittCnt': 713}},
#     '2021-08-26': {
#         'human': {'writeCnt': 6, 'likeCnt': 7, 'retwittCnt': 17},
#         'sell_coupons': {'writeCnt': 3, 'likeCnt': 0, 'retwittCnt': 713}},
#     '2021-08-25': {
#         'human': {'writeCnt': 6, 'likeCnt': 7, 'retwittCnt': 17},
#         'sell_coupons': {'writeCnt': 3, 'likeCnt': 0, 'retwittCnt': 713}},
#     '2021-08-24': {
#         'human': {'writeCnt': 6, 'likeCnt': 7, 'retwittCnt': 17}, 
#         'sell_coupons': {'writeCnt': 3, 'likeCnt': 0, 'retwittCnt': 713}}, 
#     '2021-08-23': {
#         'human': {'writeCnt': 6, 'likeCnt': 7, 'retwittCnt': 17},
#         'sell_coupons': {'writeCnt': 3, 'likeCnt': 0, 'retwittCnt': 713}},
#     '2021-08-22': {
#         'human': {'writeCnt': 6, 'likeCnt': 7, 'retwittCnt': 17},
#         'sell_coupons': {'writeCnt': 3, 'likeCnt': 0, 'retwittCnt': 713}}
# }