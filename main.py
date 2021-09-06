import sys
from datetime import datetime, timedelta
import json

# python-twitter
import twitter
from twitter import Status
# API KEY
import secrets
# 필터 문자열
import constant

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

def update_twitt_detail_info(status, user_name, twitt_user_info):
    """
    desc : Update 상세정보 - 트윗수, 좋아요수, 리트윗수
    parms: 날짜존재여부, 시간존재여부, 일시, TwittRowInfo, 계정유형(normal, ads), 일자별트윗정보, 시간별트윗정보, 계정유형별트윗정보
    """
    twitt_detail_info = twitt_user_info.get(user_name)

    twitt_detail_info['write_count'] += 1
    twitt_detail_info['like_count'] += status.favorite_count
    twitt_detail_info['retwitt_count'] += status.retweet_count

def create_twitt_info(create_at, status, user_type, twitt_days_info, twitt_hours_info, twitt_user_info, **exsits):
    """
    desc : 트윗정보 생성 - 일자별트윗정보, 시간별트윗정보, 계정유형별트윗정보, 상세트윗정보
    parms: 날짜존재여부, 시간존재여부, 일시, TwittRowInfo, 계정유형(normal, ads), 일자별트윗정보, 시간별트윗정보, 계정유형별트윗정보
    """
    # 트윗일자
    create_at_date = create_at.strftime('%Y-%m-%d')

    # Create 상세정보 - 트윗수, 좋아요수
    twitt_detail_info = {
            # 트윗수
            'write_count': 1,
            # 좋아요수
            'like_count': status.favorite_count,
            # 리트윗수
            'retwitt_count': status.retweet_count
    }
    # 계정유형별 자료 추가
    twitt_user_info[user_type] = twitt_detail_info

    if not exsits['hour_exists']:
        # 시간별 자료 추가
        twitt_hours_info[create_at.strftime('%H')] = twitt_user_info

    if not exsits['date_exists']:
        # 일자별 자료 추가
        twitt_days_info[create_at_date] = twitt_hours_info


def get_search_twitt_by_keyword(twitter_api, keyword):
    # 키워드로 검색하기 - 검색어, 100건, 최근, json파일반환
    # statuses = twitter_api.GetSearch(term=keyword, count=100, result_type="recent", return_json=True, since='2021-08-29', until='2021-09-01')
    statuses = twitter_api.GetSearch(term=keyword, count=100, result_type="recent", return_json=True)

    # 검색결과 파일 저장
    outfile = open("C:\GitHub\VNTG-N-ERP\emws\history\{}.json".format(datetime.strftime(now_time, '%y%m%d%H%M%S')), 'w')
    json.dump(statuses, outfile)

    # 리스트 변환
    statuses = [Status.NewFromJsonDict(x) for x in statuses.get('statuses', '')]

    return statuses

def main(keyword):
    # twitter api 연동시작
    twitter_api = twitter.Api(consumer_key=secrets.TWITTER_CONSUMER_KEY,
                              consumer_secret=secrets.TWITTER_CONSUMER_SECRET, 
                              access_token_key=secrets.TWITTER_ACCESS_TOKEN, 
                              access_token_secret=secrets.TWITTER_ACCESS_SECRET)

    # 키워드로 검색하기
    statuses = get_search_twitt_by_keyword(twitter_api, keyword)

    # 일자별 트윗 정보 {'일자' : {'시간': {'캠페인': {'게시글수':0, '좋아요수':0, '리트윗수':0}}}}
    twitt_days_info = {}

    # 검색 내용 출력
    for status in statuses:

        # 트윗일시
        create_at = datetime.strptime(status.created_at,'%a %b %d %H:%M:%S +0000 %Y') + timedelta(hours=9)
        # 트윗일자
        create_at_date = create_at.strftime('%Y-%m-%d')

        # 광고성 계정인지 확인
        filter_list = [element for element in constant.C_FILTER_KEYWORD if(element in status.user.name)]
        # 계정
        user_type = 'ads' if bool(filter_list) is True else 'normal'

        # 일자별 트윗 정보가 존재하는지 확인
        if create_at_date in twitt_days_info:
            ##### 일자별 트윗 정보 존재
            # 일자별 정보 가져오기
            twitt_hours_info = twitt_days_info.get(create_at_date)

            # 시간별 트윗 정보가 존재하는지 확인
            if create_at.strftime('%H') in twitt_hours_info:
                ##### 시간별 트윗 정보가 존재
                twitt_user_info = twitt_hours_info.get(create_at.strftime('%H'))
                
                # 사용자가 이미 저장되었는지 확인
                if user_type in twitt_user_info:
                    # 상세정보 업데이트 - 트윗수, 좋아요수, 리트윗수
                    update_twitt_detail_info(status, user_type, twitt_user_info)
                    
                else:
                    # 일자별, 시간별, 사용자별 자료 생성
                    create_twitt_info(create_at, status, user_type, twitt_days_info, twitt_hours_info, twitt_user_info, date_exists=True, hour_exists=True)

            else:
                ##### 시간별 트윗 정보가 미존재
                # 새로운 시간을 위한 정보
                twitt_user_info = {}

                # 일자별, 시간별, 사용자별 자료 생성
                create_twitt_info(create_at, status, user_type, twitt_days_info, twitt_hours_info, twitt_user_info, date_exists=True, hour_exists=False)
            
        else:
            ##### 일자별 트윗 정보 미존재
            twitt_user_info = {}
            twitt_hours_info = {}

            # 일자별, 시간별, 사용자별 자료 생성
            create_twitt_info(create_at, status, user_type, twitt_days_info, twitt_hours_info, twitt_user_info, date_exists=False, hour_exists=False)

        # # print(status)
        print('-----------')
        print('id_str : ' + status.id_str)
        print('name : ' + status.user.name)
        print('screen_name : ' + status.user.screen_name)
        print('hashtags : ' + str(status.hashtags))
        print('favorite_count : ' + str(status.favorite_count))
        print('retweet_count : ' + str(status.retweet_count))
        print('create_at : ' + str(create_at))
        # # print(status.text.encode('utf-8'))
        # print('text : ' + status.text)

    print('')
    print(f"검색어 '{keyword}'로 검색된 건수 : {len(statuses)}건")
    print(twitt_days_info)
    # print('-------------')
    # print(list(twitt_days_info.items()))

    # 자료 저장(스프레드시트) 및 메일 발송(gmail)
    save_data_on_spreadsheet(twitt_days_info)

def save_data_on_spreadsheet(twitt_days_info):
    """구글스프레드시트 저장"""
    scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
    ]

    json_file_name = 'C:\GitHub\VNTG-N-ERP\emws\gspread.json'

    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
    gc = gspread.authorize(credentials)


    spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1Z5yePPQLSJOpPxAOHWv4mTQJXxw_vUEjIFKBcqIzqA0/edit#gid=0'

    # 스프레스시트 문서 가져오기 
    doc = gc.open_by_url(spreadsheet_url)

    # 스프레드시트 문서명
    # worksheetName = datetime.strftime(now_time, '%Y%m')
    worksheetName = f'{now_time.year}{str(now_time.month).zfill(2)}'

    # 시트 선택하기
    worksheet = doc.worksheet(worksheetName)

    # 시트 자료 가져오기
    worksheet_datas = worksheet.get_all_records()

    # 1일이면 시트 생성
    if now_time.day == 1:
        # 시트 생성
        worksheet = doc.add_worksheet(title=worksheetName, rows='1000', cols='22')
        # 타이틀 추가
        worksheet.append_row(constant.C_SPREADSHEET_TITLE)
    
    # 스프레드시트 작성
    for post_date, hour_data in sorted(twitt_days_info.items()):
        # print(post_date, hour_data)
        for post_hour, campaign_data in sorted(hour_data.items()):
            # print(post_date, post_hour, campaign_data)
            for campaign, post_data in campaign_data.items():

                # 추가 작성 필요 여부
                appendYN = True

                # 스프레드시트 내용 확인
                for worksheet_data in worksheet_datas:
                    # 스프레드시트의 일자/시간과 수집한 일자/시간과 일치하는지 확인
                    if worksheet_data['게시일자'] == str(post_date) and worksheet_data['시간(24시)'] == int(post_hour):
                        ##### 업데이트 필요
                        # print('존재')
                        appendYN = False

                        # 스프레드시트 행 수 ( +2 : 인덱스 0부터 시작 / 타이틀 )
                        rowCnt = worksheet_datas.index(worksheet_data) + 2

                        # 스프레드시트 열
                        colName = "H"

                        # 게시일자 + n일이 수집일자와 같은지 확인
                        for i in range(0, 7):
                            if (datetime.strptime(worksheet_data['게시일자'], '%Y-%m-%d') + timedelta(days=i+1) == 
                                datetime.strptime(datetime.strftime(now_time, '%Y-%m-%d'), '%Y-%m-%d')):
                                # print('게시일자 + {}일이 수집일자와 동일'.format(i+1))
                                colName = chr(ord(colName) + i)

                                # 스프레드시트 작성
                                worksheet.update_acell(f'{colName}{rowCnt}', list(post_data.values())[1] + list(post_data.values())[2])

                                pass

                if appendYN == True:
                    ##### 신규 건 스프레드시트 작성
                    print('신규')
                    # 작성
                    worksheet.append_row([
                                        #   datetime.strftime(now_time, '%Y-%m-%d %H:%M:%S')
                                        datetime.strftime(now_time, '%Y-%m-%d %H')
                                        , str(post_date)
                                        , str(post_hour)
                                        , str(campaign)
                                        , list(post_data.values())[0]
                                        , list(post_data.values())[1]
                                        , list(post_data.values())[2]
                                        , "", "", "", "", "", "", ""
                                        , "추가"
                                        ])

    print('스프레드시트 작성 종료')

    # 메일 발송
    send_email_result = send_email.send_email(constant.C_ADMIN_MAIL_ADDRESS)

    print(f'메일 발송 결과 : {send_email_result}')

if __name__ == '__main__':

    # 기본 검색어
    keywordsimple = '에피민트'
    keyword = f'({keywordsimple} OR #{keywordsimple})'
    # 확장 검색어 - 리트윗 제외
    extword = 'AND exclude:retweets'
    # extword = 'AND exclude:retweets AND filter:quote'
    # Full 검색키워드
    full_keyword = f'{keyword} {extword}'

    # 파라미터가 있는지 확인 - 없으면 기본 : '에피민트'
    if len(sys.argv) == 1:
        sys.argv.append(full_keyword)
    else:
        full_keyword = f'({sys.argv[1]} OR #{sys.argv[1]}) {extword}'

    # sys.argv.append(full_keyword) if len(sys.argv) == 1 else full_keyword = '{} {}'.format(sys.argv[1], extword)

    # 현재일시
    now_time = datetime.now()

    # main 호출
    main(full_keyword)
    # main_test1(keyword)
    # main_test2(keyword)

def main_test1(keyword):
    # twitter api 연동시작
    twitter_api = twitter.Api(consumer_key=secrets.TWITTER_CONSUMER_KEY,
                            consumer_secret=secrets.TWITTER_CONSUMER_SECRET, 
                            access_token_key=secrets.TWITTER_ACCESS_TOKEN, 
                            access_token_secret=secrets.TWITTER_ACCESS_SECRET)

    # 키워드로 검색하기
    statuses = get_search_twitt_by_keyword(twitter_api, keyword)

    # 일자별 트윗 정보 { '일자' : {[게시글수, 좋아요수, 리트윗수]}}
    twitt_days_info = {}

    # 검색 내용 출력
    for status in statuses:

        # 트윗일시
        create_at = datetime.strptime(status.created_at,'%a %b %d %H:%M:%S +0000 %Y') + timedelta(hours=9)
        # 트윗일자
        create_at_date = create_at.strftime('%Y-%m-%d')

        # 일자별 트윗 정보에 존재하는지 확인
        if create_at_date in twitt_days_info:
            print('존재 : ' + create_at_date)

            # 조회된 정보 가져오기 및 누적
            twitt_detail_info = twitt_days_info.get(create_at_date)

            twitt_detail_info['write_count'] += 1
            twitt_detail_info['like_count'] = twitt_detail_info['like_count'] +  status.favorite_count
            twitt_detail_info['retwitt_count'] = twitt_detail_info['retwitt_count'] +  status.retweet_count
            
        else:
            print('미존재 : ' + create_at_date)
            
            # 상세정보 - 트윗수, 좋아요수
            twitt_detail_info = {
                                # 트윗수
                                'write_count': 1,
                                # 좋아요수
                                'like_count': status.favorite_count,
                                # 리트윗수
                                'retwitt_count': status.retweet_count
                            }

            # 일자별 상세정보 Dictionary
            twitt_days_info[create_at_date] = twitt_detail_info

    print("'{}'로 검색된 건수 : {}건".format(keyword, len(statuses)))
    print(twitt_days_info)

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
        # 트윗
        twitterPost = twittPostInfo(status.id_str,
                                    {
                                    'create_at': create_at,
                                    'create_at_date': create_at_date,
                                    'user_name': status.user.name, 
                                    'user_screen_name': status.user.screen_name,
                                    'text': status.text,
                                    'favorite_count': status.favorite_count,
                                    'retweet_count': status.retweet_count,
                                    })

        twittInfolist.append(twitterPost)

    # print(twittInfolist)
    # print('-------------')
    for twittInfo in twittInfolist:
        print(twittInfo)
        # twittInfo.get_favorite_count()

    print('-------------')
    # collectInfo = {}

    # for twittInfo in twittInfolist:
        
    #     collectHourlyInfo = {}

    #     for i in range(0, 24, 1):

    #         if int(twittInfo._details['create_at'].strftime('%H')) == i:

    #             if int(twittInfo._details['create_at'].strftime('%H')) in collectHourlyInfo:
    #                 pass
    #             else:
    #                 collectHourlyInfo[i] = {
    #                                         # 트윗수
    #                                         'write_count': 1,
    #                                         # 좋아요수
    #                                         'like_count': status.favorite_count,
    #                                         # 리트윗수
    #                                         'retwitt_count': status.retweet_count
    #                                         }
    #                 if twittInfo._details['create_at_date'] in collectInfo:
    #                     collectInfo = collectInfo.get(twittInfo._details['create_at_date'])
    #                 else:                    
    #                     collectInfo[twittInfo._details['create_at_date']] = collectHourlyInfo[i]

    # print(collectInfo)

    # save_data_on_spreadsheet(twittInfolist)