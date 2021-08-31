import sys
import twitter
import datetime
# API KEY
import secrets
# 필터 문자열
import constant

class twittPostInfo():
    """
    twittInfo Class
    Author : 현이
    Data: 2021.08.31
    사용법: 'ID', {'게시일시', '게시일자', '사용자ID', '사용자계정', '내용', '좋아요수', '리트윗수'}
    """
    # 트윗 개수
    twitt_hourly_post_count = 0
    twitt_hourly_like_count = 0
    twitt_hourly_retw_count = 0

    # def __init__(self, id_str, create_at, create_date, create_hour, user_name, user_screen_name, favorite_count, retweet_count, text):
    def __init__(self, id_str, details):
        self._id_str = id_str
        self._details = details

    def __str__(self):
        return 'str : {} - {}'.format(self._id_str, self._details)

    def __repr__(self):
        return 'repr : {} - {}'.format(self._id_str, self._details)

    def detail_info(self):
        print('Current ID : {}'.format(id(self)))
        print('Twitt Detail Info : {} {}'.format(self._id_str, self._details.get('favorite_count')))

    def get_favorite_count(self):
        return self._details.get('favorite_count')

    def get_retweet_count(self):
        return self._details.get('retweet_count')


def updateTwittDetailInfo(status, user_name, twittUserInfo):
    # Update 상세정보 - 트윗수, 좋아요수
    twittDetailInfo = twittUserInfo.get(user_name)

    twittDetailInfo['writeCnt'] += 1
    twittDetailInfo['likeCnt'] += status.favorite_count
    twittDetailInfo['retwittCnt'] += status.retweet_count

def createTwittInfo(dateExists, create_at, status, user_name, twittDaysInfo, twittUserInfo):
    # 트윗일자
    create_at_date = create_at.strftime('%Y-%m-%d')

    # Create 상세정보 - 트윗수, 좋아요수
    twittDetailInfo = {
            # 트윗수
            'writeCnt': 1,
            # 좋아요수
            'likeCnt': status.favorite_count,
            # 리트윗수
            'retwittCnt': status.retweet_count
    }
    twittUserInfo[user_name] = twittDetailInfo

    # twittHourlyInfo = {}

    # # 시간별 자료가 있는지 확인
    # if create_at.strftime('%H') in twittHourlyInfo:
    #     twittHourlyInfo = twittHourlyInfo.get(create_at.strftime('%H'))
    
    if dateExists == False:
        twittDaysInfo[create_at_date] = twittUserInfo

        # twittHourlyInfo[create_at.strftime('%H')] = twittUserInfo
        # twittDaysInfo[create_at_date] = twittHourlyInfo

    # return twittDaysInfo


def getSearchTwittbyKeyword(twitter_api, keyword):
    # 키워드로 검색하기
    statuses = twitter_api.GetSearch(term=keyword, count=100, result_type="recent")

    return statuses

def main(keyword):
    # twitter api 연동시작
    twitter_api = twitter.Api(consumer_key=secrets.TWITTER_CONSUMER_KEY,
                            consumer_secret=secrets.TWITTER_CONSUMER_SECRET, 
                            access_token_key=secrets.TWITTER_ACCESS_TOKEN, 
                            access_token_secret=secrets.TWITTER_ACCESS_SECRET)

    # 키워드로 검색하기
    statuses = getSearchTwittbyKeyword(twitter_api, keyword)

    # # 검색하기 - 파일 저장
    # import json
    # statuses = twitter_api.GetSearch(term=query, count=100, result_type="recent", return_json=True)

    # with open("./sample.json", 'w') as outfile:
    #     json.dump(statuses, outfile)

    # 일자별 트윗 정보 { '일자' : {'계정': {[게시글수, 좋아요수, 리트윗수]}}}
    twittDaysInfo = {}

    # 검색 내용 출력
    for status in statuses:
        
        # 트윗일시
        create_at = datetime.datetime.strptime(status.created_at,'%a %b %d %H:%M:%S +0000 %Y') + datetime.timedelta(hours=9)
        # 트윗일자
        create_at_date = create_at.strftime('%Y-%m-%d')

        # 일자별 트윗 정보에 존재하는지 확인
        if create_at_date in twittDaysInfo:
            # print('존재 : ' + create_at_date)

            # 조회된 정보 가져오기 및 누적
            twittUserInfo = twittDaysInfo.get(create_at_date)

            # 필터 문자열
            for filterStr in constant.C_FILTER_KEYWORD:
                # 사용자가 필터 문자열에 포함되는지 확인
                if filterStr in status.user.name:
                    # 사용자가 이미 저장되었는지 확인
                    if status.user.screen_name in twittUserInfo:
                        # 상세정보 - 트윗수, 좋아요수
                        updateTwittDetailInfo(status, status.user.screen_name, twittUserInfo)
                        
                    else:
                        # 상세정보 - 트윗수, 좋아요수
                        createTwittInfo(True, create_at, status, status.user.screen_name, twittDaysInfo, twittUserInfo)

                else:
                    if 'normal' in twittUserInfo:
                        # 상세정보 - 트윗수, 좋아요수
                        updateTwittDetailInfo(status, 'normal', twittUserInfo)
                                                
                    else:
                        # 상세정보 - 트윗수, 좋아요수
                        createTwittInfo(True, create_at, status, 'normal', twittDaysInfo, twittUserInfo)
            
        else:
            # print('미존재 : ' + create_at_date)

            twittUserInfo = {}
            
            # 필터 문자열
            for filterStr in constant.C_FILTER_KEYWORD:

                # 사용자가 필터 문자열에 포함되는지 확인
                if filterStr in status.user.name:
                    # 상세정보 - 트윗수, 좋아요수
                    createTwittInfo(False, create_at, status, status.user.screen_name, twittDaysInfo, twittUserInfo)

                else:
                    # 상세정보 - 트윗수, 좋아요수
                    createTwittInfo(False, create_at, status, 'normal', twittDaysInfo, twittUserInfo)

        # print(status)
        # print('-----------')
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
    # print('-------------')
    # print(list(twittDaysInfo.items()))

    # for detail in twittDaysInfo:
    #     print(twittDaysInfo.get(detail))
    #     for detail1 in twittDaysInfo.get(detail):
    #         print(twittDaysInfo.get(detail).get(detail1))
    
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


import gspread
from oauth2client.service_account import ServiceAccountCredentials

def saveData(twittInfolist):
    scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
    ]

    json_file_name = 'gspread.json'

    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
    gc = gspread.authorize(credentials)


    spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1Z5yePPQLSJOpPxAOHWv4mTQJXxw_vUEjIFKBcqIzqA0/edit#gid=0'

    # 스프레스시트 문서 가져오기 
    doc = gc.open_by_url(spreadsheet_url)

    # 시트 선택하기
    worksheet = doc.worksheet('시트1')




def main_test2(keyword):
    # twitter api 연동시작
    twitter_api = twitter.Api(consumer_key=secrets.TWITTER_CONSUMER_KEY,
                            consumer_secret=secrets.TWITTER_CONSUMER_SECRET, 
                            access_token_key=secrets.TWITTER_ACCESS_TOKEN, 
                            access_token_secret=secrets.TWITTER_ACCESS_SECRET)

    # 키워드로 검색하기
    statuses = getSearchTwittbyKeyword(twitter_api, keyword)

    # 트윗 리스트
    twittInfolist = []

    # 검색 내용 출력
    for status in statuses:

        # 트윗일시
        create_at = datetime.datetime.strptime(status.created_at,'%a %b %d %H:%M:%S +0000 %Y') + datetime.timedelta(hours=9)
        # 트윗일자
        create_at_date = create_at.strftime('%Y-%m-%d')

        twittercls = twittPostInfo(status.id_str,
                                    {
                                    'create_at': create_at,
                                    'create_at_date': create_at_date,
                                    'user_name': status.user.name, 
                                    'user_screen_name': status.user.screen_name,
                                    'text': status.text,
                                    'favorite_count': status.favorite_count,
                                    'retweet_count': status.retweet_count,
                                    })

        twittInfolist.append(twittercls)

    # print(twittInfolist)
    # print('-------------')
    for twittInfo in twittInfolist:
        print(twittInfo)
        # twittInfo.get_favorite_count()

    print('-------------')
    collectInfo = {}

    for twittInfo in twittInfolist:
        
        collectHourlyInfo = {}

        for i in range(0, 24, 1):

            if int(twittInfo._details['create_at'].strftime('%H')) == i:

                if int(twittInfo._details['create_at'].strftime('%H')) in collectHourlyInfo:
                    pass
                else:
                    collectHourlyInfo[i] = {
                                            # 트윗수
                                            'writeCnt': 1,
                                            # 좋아요수
                                            'likeCnt': status.favorite_count,
                                            # 리트윗수
                                            'retwittCnt': status.retweet_count
                                            }
                    if twittInfo._details['create_at_date'] in collectInfo:
                        collectInfo = collectInfo.get(twittInfo._details['create_at_date'])
                    else:                    
                        collectInfo[twittInfo._details['create_at_date']] = collectHourlyInfo[i]

    print(collectInfo)

    saveData(twittInfolist)


if __name__ == '__main__':

    # 파라미터가 있는지 확인 - 없으면 기본 : '에피민트'
    if len(sys.argv) == 1:
        sys.argv.append('에피민트')

    print('-----------')

    # main 실행
    main(sys.argv[1])
    # main_test1(sys.argv[1])
    # main_test2(sys.argv[1])

    
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