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

# 구글 스프레드시트
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 이메일 발송
import send_email

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

    def __init__(self, id_str, details):
        self._id_str = id_str
        self._details = details

    def __str__(self):
        return 'str : {} - {}'.format(self._id_str, self._details)

    def __repr__(self):
        return 'repr : {} - {}'.format(self._id_str, self._details)

    def detail_info(self):
        print('Current ID : {}'.format(id(self)))
        print('Twitt Detail Info : {} {} {}'.format(self._id_str, self._details.get('favorite_count'), self._details.get('retweet_count')))

    def get_favorite_count(self):
        return self._details.get('favorite_count')

    def get_retweet_count(self):
        return self._details.get('retweet_count')

def get_search_twitt_by_keyword(twitter_api, keyword):
    # 키워드로 검색하기 - 검색어, 100건, 최근, json파일반환
    # statuses = twitter_api.GetSearch(term=keyword, count=100, result_type="recent", return_json=True, since='2021-08-29', until='2021-09-01')
    statuses = twitter_api.GetSearch(term=keyword, count=100, result_type="recent", return_json=True)

    # 검색결과 파일 저장
    outfile = open(common.resource_path('history\{}.json').format(datetime.strftime(now_time, '%y%m%d%H%M%S')), 'w')
    # outfile = open(f"{constant.C_ROOT_PATH}\history\{datetime.strftime(now_time, '%y%m%d%H%M%S')}.json", 'w')
    json.dump(statuses, outfile)

    # 리스트 변환
    statuses = [Status.NewFromJsonDict(x) for x in statuses.get('statuses', '')]

    return statuses

def main_test1(keyword):
    # twitter api 연동시작
    twitter_api = twitter.Api(consumer_key=secrets.TWITTER_CONSUMER_KEY,
                              consumer_secret=secrets.TWITTER_CONSUMER_SECRET, 
                              access_token_key=secrets.TWITTER_ACCESS_TOKEN, 
                              access_token_secret=secrets.TWITTER_ACCESS_SECRET)

    # 키워드로 검색하기
    statuses = get_search_twitt_by_keyword(twitter_api, keyword)

    # 일자별 트윗 정보 []
    collect_list = {}

    # 검색 내용 출력
    for status in statuses:

        # 트윗일시
        create_at = datetime.strptime(status.created_at,'%a %b %d %H:%M:%S +0000 %Y') + timedelta(hours=9)
        # 트윗일자
        create_at_date = create_at.strftime('%Y-%m-%d')

        # 광고성 계정인지 확인
        filter_list = [element for element in constant.C_FILTER_KEYWORD if(element in status.user.name)]
        # 계정
        ads_yn = 'ads' if bool(filter_list) is True else 'normal'

        # id_str	create_at	user_name	user_name	user_screen_name	favorite_count	retweet_count	text	ads_yn
        # collect_list.append([status.id_str, create_at, create_at_date, status.user.name, status.user.screen_name, status.favorite_count, status.retweet_count, status.text, ads_yn])
        collect_list[status.id_str] = [create_at, create_at_date, status.user.name, status.user.screen_name, status.favorite_count, status.retweet_count, status.text, ads_yn]

        # # print(status)
        print('create_at : ' + str(create_at))
        print('id_str : ' + status.id_str)
        print('name : ' + status.user.name)
        print('screen_name : ' + status.user.screen_name)
        print('favorite_count : ' + str(status.favorite_count))
        print('retweet_count : ' + str(status.retweet_count))
        print('text : ' + status.text)
        # print('hashtags : ' + str(status.hashtags))
        # print(status.text.encode('utf-8'))
        print('--------------------------------------------------')

    print(f"검색어 '{keyword}'로 검색된 건수 : {len(statuses)}건")
    print(collect_list)

def main_test2(keyword):
    # twitter api 연동시작
    twitter_api = twitter.Api(consumer_key=secrets.TWITTER_CONSUMER_KEY,
                            consumer_secret=secrets.TWITTER_CONSUMER_SECRET, 
                            access_token_key=secrets.TWITTER_ACCESS_TOKEN, 
                            access_token_secret=secrets.TWITTER_ACCESS_SECRET)

    # 키워드로 검색하기
    statuses = get_search_twitt_by_keyword(twitter_api, keyword)

    # 트윗 리스트
    twittInfolist = []

    # 검색 내용 출력
    for status in statuses:

        # 트윗일시
        create_at = datetime.strptime(status.created_at,'%a %b %d %H:%M:%S +0000 %Y') + timedelta(hours=9)
        # 트윗일자
        create_at_date = create_at.strftime('%Y-%m-%d')

        # 광고성 계정인지 확인
        filter_list = [element for element in constant.C_FILTER_KEYWORD if(element in status.user.name)]
        # 게시글 유형
        post_type = 'ads' if bool(filter_list) is True else 'normal'

        twittercls = twittPostInfo(status.id_str,
                                    {
                                    'create_at': create_at.strftime('%Y-%m-%d %H:%M:%S'),
                                    'create_at_date': create_at_date,
                                    'user_name': status.user.name, 
                                    'user_screen_name': status.user.screen_name,
                                    'text': status.text,
                                    'favorite_count': status.favorite_count,
                                    'retweet_count': status.retweet_count,
                                    'post_type': post_type
                                    })

        twittInfolist.append(twittercls)

    # # print(twittInfolist)
    # print('-------------')
    # for twittInfo in twittInfolist:
    #     # print(type(twittInfo._details.values()))
    #     # print( list(zip(twittInfo._id_str,twittInfo._details.values())) )

    #     # print( list(zip(twittInfo._details.keys(),twittInfo._details.values())) )
    #     # print(type(list(twittInfo._details.values())))
    #     test_list = list(twittInfo._details.values())
    #     test_list.insert(0, twittInfo._id_str)
    #     print(test_list)
    
    gspreadDoc = get_spreadsheet()    

    # # 시트 선택하기 - master
    # mastersheet = gspreadDoc.worksheet('master')
    # save_data_on_spreadsheet(mastersheet, twittInfolist)

    # 시트 선택하기 - deteail
    detailsheet = gspreadDoc.worksheet('detail')
    save_data_on_spreadsheet(detailsheet, twittInfolist)

def get_spreadsheet():
    """구글스프레드시트 저장"""
    scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
    ]

    json_file_name = common.resource_path('gspread.json')
    # json_file_name = f'{constant.C_ROOT_PATH}\gspread.json'

    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
    gc = gspread.authorize(credentials)


    spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1Z5yePPQLSJOpPxAOHWv4mTQJXxw_vUEjIFKBcqIzqA0/edit#gid=0'

    # 스프레스시트 문서 가져오기 
    return gc.open_by_url(spreadsheet_url)

def save_data_on_spreadsheet(worksheet, twittInfolist):

    if worksheet.title == 'master':
        for item in twittInfolist:
            list_item = list(item._details.values())
            list_item.insert(0, item._id_str)
            worksheet.append_row(list_item)

    if worksheet.title == 'detail':
        for item in twittInfolist:
            # print(now_time.strftime('%Y-%m-%d %H:%M:%S'), item._id_str, item.get_favorite_count(), item.get_retweet_count())
            list_item = [now_time.strftime('%Y-%m-%d %H:%M:%S'), item._id_str, item.get_favorite_count(), item.get_retweet_count()]
            worksheet.append_row(list_item)

    print('master - 스프레드시트 작성 종료')


if __name__ == '__main__':

    # 현재일시
    now_time = datetime.now()

    # # 로그
    # logger = logging.getLogger("mainLog")
    # logger.setLevel(logging.INFO)
    # loggerHandler = logging.StreamHandler()

    # formatter = logging.Formatter('%(asctime)s|%(name)s|%(levelname)s:%(message)s')
    # loggerHandler.setFormatter(formatter)
    # logger.addHandler(loggerHandler)

    # # Create Handeler == 로깅한 정보가 출력되는 위치 설정
    # streamHandler = logging.StreamHandler()
    # streamHandler.setLevel(logging.DEBUG)
    # streamHandler.setFormatter(formatter)
    # # logger.addHandler(streamHandler)

    # logfile_path = '{}\log\{}.log'.format(common.resource_path(''), datetime.strftime(now_time, '%y%m%d%H%M%S'))
    # # logfile_path = '{}\log\{}.log'.format(constant.C_ROOT_PATH, datetime.strftime(now_time, '%y%m%d%H%M%S'))

    # fileHandler = logging.FileHandler(logfile_path, encoding='utf8')
    # fileHandler.setLevel(logging.DEBUG)
    # fileHandler.setFormatter(formatter)
    # logger.addHandler(fileHandler)

    print('----------------------------------------------------------------------------------------------------')
    print("start : Search twitter")
    print('----------------------------------------------------------------------------------------------------')

    # Main
    try:
        # 기본 검색어 - 해시태그 포함
        keywordsimple = '에피민트'
        keyword = f'({keywordsimple} OR #{keywordsimple})'

        # 확장 검색어 - 리트윗 제외
        keyword_ext = 'AND exclude:retweets'

        # Full 검색키워드
        full_keyword = f'{keyword} {keyword_ext}'

        # 파라미터가 있는지 확인 - 없으면 기본 : '에피민트'
        if len(sys.argv) == 1:
            sys.argv.append(full_keyword)
        else:
            full_keyword = '({} OR #{}) {}'.format(sys.argv[1], sys.argv[1], keyword_ext)

        # main 호출
        # main(full_keyword)
        # main_test1(full_keyword)
        main_test2(full_keyword)

    except Exception as inst:
        print("error" + str(inst))

    print('----------------------------------------------------------------------------------------------------')
    print("end : Search twitter")
    print('----------------------------------------------------------------------------------------------------')