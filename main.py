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

    # def __init__(self, id_str, create_at, create_date, create_hour, user_name, user_screen_name, favorite_count, retweet_count, text):
    def __init__(self, id_str, details):
        self._id_str = id_str
        self._details = details

    def __str__(self):
        return 'str : {} - {}'.format(self._id_str, self._details)

    def __repr__(self):
        return 'repr : {} - {}'.format(self._id_str, self._details)

    def detail_info(self):
        logger.info('Current ID : {}'.format(id(self)))
        logger.info('Twitt Detail Info : {} {}'.format(self._id_str, self._details.get('favorite_count')))

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
            'retwitt_count': status.retweet_count,
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
    outfile = open(common.resource_path('history\{}.json').format(datetime.strftime(now_time, '%y%m%d%H%M%S')), 'w')
    # outfile = open(f"{constant.C_ROOT_PATH}\history\{datetime.strftime(now_time, '%y%m%d%H%M%S')}.json", 'w')
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

        # # logger.info(status)
        logger.info('create_at : ' + str(create_at))
        logger.info('id_str : ' + status.id_str)
        logger.info('name : ' + status.user.name)
        logger.info('screen_name : ' + status.user.screen_name)
        logger.info('favorite_count : ' + str(status.favorite_count))
        logger.info('retweet_count : ' + str(status.retweet_count))
        logger.info('text : ' + status.text)
        # logger.info('hashtags : ' + str(status.hashtags))
        # logger.info(status.text.encode('utf-8'))
        logger.info('--------------------------------------------------')

    logger.info(f"검색어 '{keyword}'로 검색된 건수 : {len(statuses)}건")
    logger.info(twitt_days_info)
    # logger.info('-------------')
    # logger.info(list(twitt_days_info.items()))

    # 자료 저장(스프레드시트) 및 메일 발송(gmail)
    save_data_on_spreadsheet(twitt_days_info)

def save_data_on_spreadsheet(twitt_days_info):
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
    doc = gc.open_by_url(spreadsheet_url)

    # 스프레드시트 문서명
    # worksheetName = f'{now_time.year}{str(now_time.month).zfill(2)}의 사본'
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

     # 신규 행 추가 필요 여부
    new_row_yn = True;
    # 트윗수 누적, 좋아요수 누적, 리트윗수 누적
    write_count_cumul = 0
    like_count_cumul = 0
    retwitt_count_cumul = 0
    write_count_cumul_prev = 0
    like_count_cumul_prev = 0
    retwitt_count_cumul_prev = 0

    # 스프레드 마지막 시트 자료
    worksheet_data_last = worksheet_datas[len(worksheet_datas) - 1]

    # 전일 정보
    last_row_list = [worksheet_data for worksheet_data in worksheet_datas 
                if (datetime.strftime(now_time + timedelta(days=-1), '%Y-%m-%d') in worksheet_data['게시일자'])]

    # 전일 마지막 행
    last_row = last_row_list[len(last_row_list) - 1]
    
    # 스프레드시트 작성
    for post_date, hour_data in sorted(twitt_days_info.items()):
        # logger.info(post_date, hour_data)
        for post_hour, campaign_data in sorted(hour_data.items()):
            # logger.info(post_date, post_hour, campaign_data)
            for campaign, post_data in campaign_data.items():

                # 추가 작성 필요 여부
                appendYN = True

                # 이전일자 - 기본 값
                prev_post_date = '1111-01-01'
                # 일자 개수
                day_count = 0

                # 스프레드시트 내용 확인
                for worksheet_data in worksheet_datas:

                    day_count = day_count + 1 if prev_post_date == worksheet_data['게시일자'] else 0
                    prev_post_date = worksheet_data['게시일자']
                    # 스프레드시트 행 수 ( +2 : 인덱스 0부터 시작 / 타이틀 )
                    rowCnt = worksheet_datas.index(worksheet_data) + 2

                    # 스프레드시트의 일자/시간과 수집한 일자/시간과 일치하는지 확인
                    if (worksheet_data['게시일자'] == str(post_date) and
                        worksheet_data['시간(24시)'] == int(post_hour) and
                        worksheet_data['채널'] == campaign):
                        ##### 업데이트 필요
                        # 같은 일자 누적 자료 갱신
                        # if (datetime.strptime(worksheet_data['게시일자'], '%Y-%m-%d')
                        if (datetime.strptime(post_date, '%Y-%m-%d')
                            == datetime.strptime(datetime.strftime(now_time, '%Y-%m-%d'), '%Y-%m-%d') + timedelta(days=-1)):
                            # print(datetime.strptime(worksheet_data['게시일자'], '%Y-%m-%d'))
                            # print(datetime.strptime(datetime.strftime(now_time, '%Y-%m-%d'), '%Y-%m-%d') + timedelta(days=-1))
                            # 하루 전 합계
                            write_count_cumul_prev += list(post_data.values())[0]
                            like_count_cumul_prev += list(post_data.values())[1]
                            retwitt_count_cumul_prev += list(post_data.values())[2]

                        # 같은 일자 누적 자료 갱신
                        if (datetime.strptime(worksheet_data['게시일자'], '%Y-%m-%d')
                            == datetime.strptime(worksheet_data_last['게시일자'], '%Y-%m-%d')):
                            # == datetime.strptime(datetime.strftime(now_time, '%Y-%m-%d'), '%Y-%m-%d')):
                            if day_count == 0:
                                # print("0 - worksheet_data['시간(24시)']" + str(worksheet_data['시간(24시)']))
                                # 일자의 첫번째 시간 : 시점과 동일
                                write_count_cumul = list(post_data.values())[0]
                                like_count_cumul = list(post_data.values())[1]
                                retwitt_count_cumul = list(post_data.values())[2]
                            else:
                                # print("else - worksheet_data['시간(24시)']" + str(worksheet_data['시간(24시)']))
                                # 일자의 두번째 이상 시간 : 누적
                                write_count_cumul += list(post_data.values())[0]
                                like_count_cumul += list(post_data.values())[1]
                                retwitt_count_cumul += list(post_data.values())[2]

                        # 마지막 열이 신규 게시물로 인해 추가된 행이 아닌 경우 업데이트
                        if (worksheet_datas.index(worksheet_data) + 1 == len(worksheet_datas) and
                            worksheet_data['수집일시'] == '{} {}'.format(worksheet_data['게시일자'], str(worksheet_data['시간(24시)']).zfill(2))):
                            # print(worksheet_data['게시일자'], ' ', worksheet_data['시간(24시)'])
                            # 수집일시 업데이트
                            worksheet.update_acell(f'A{rowCnt}', datetime.strftime(now_time, '%Y-%m-%d %H'))                
                            # 신규행 추가 불필요
                            new_row_yn = False

                            # 여러셀 업데이트
                            cell_list = worksheet.range('E{}:L{}'.format(rowCnt, rowCnt))

                            cell_values = [list(post_data.values())[0],
                                           list(post_data.values())[1], 
                                           list(post_data.values())[2], 
                                           write_count_cumul, 
                                           like_count_cumul, 
                                           retwitt_count_cumul,
                                           like_count_cumul_prev - last_row['좋아요 누적수(D)'],
                                           retwitt_count_cumul_prev - last_row['리트윗 누적수(D)']
                                           ]

                            for i, val in enumerate(cell_values):
                                cell_list[i].value = val

                            worksheet.update_cells(cell_list)

                        # 신규 추가 여부
                        appendYN = False

                        # 스프레드시트 열
                        colName = "M"

                        # 게시일자 + n일이 수집일자와 같은지 확인
                        for i in range(0, 7):
                            if (datetime.strptime(worksheet_data['게시일자'], '%Y-%m-%d') + timedelta(days=i+1) == 
                                datetime.strptime(worksheet_data_last['게시일자'], '%Y-%m-%d') ):
                                # logger.info('게시일자 + {}일이 수집일자와 동일'.format(i+1))
                                colName = chr(ord(colName) + i)

                                # 스프레드시트 작성 - 좋아요수 + 리트윗수
                                # print(f'{colName}{rowCnt}', list(post_data.values())[1] + list(post_data.values())[2])
                                worksheet.update_acell(f'{colName}{rowCnt}', list(post_data.values())[1] + list(post_data.values())[2])

                                pass

                if appendYN == True:
                    ##### 신규 건 스프레드시트 작성
                    # print('appendYN == True')
                    # 신규 행 추가 필요 여부
                    new_row_yn = False;

                    # # 트윗수 누적
                    # write_count_cumul += worksheet_data_last['게시물 누적수(D)'] if worksheet_data_last['게시일자'] == str(post_date) else 0
                    # # 좋아요수 누적
                    # like_count_cumul += worksheet_data_last['좋아요 누적수(D)'] if worksheet_data_last['게시일자'] == str(post_date) else 0
                    # # 리트윗수 누적
                    # retwitt_count_cumul += worksheet_data_last['리트윗 누적수(D)'] if worksheet_data_last['게시일자'] == str(post_date) else 0

                    # print('신규 건 존재')
                    worksheet.append_row([
                                          datetime.strftime(now_time, '%Y-%m-%d %H')
                                        , str(post_date)
                                        , str(post_hour)
                                        , str(campaign)
                                        , list(post_data.values())[0]
                                        , list(post_data.values())[1]
                                        , list(post_data.values())[2]
                                        , (write_count_cumul if str(post_date) == worksheet_data_last['게시일자'] else 0) + list(post_data.values())[0]
                                        , (like_count_cumul  if str(post_date) == worksheet_data_last['게시일자'] else 0) + list(post_data.values())[1]
                                        , (retwitt_count_cumul if str(post_date) == worksheet_data_last['게시일자'] else 0) + list(post_data.values())[2]
                                        , like_count_cumul_prev - last_row['좋아요 누적수(D)']
                                        , retwitt_count_cumul_prev - last_row['리트윗 누적수(D)']
                                        , "", "", "", "", "", "", ""
                                        , "신규 게시글"
                                        ])

    if new_row_yn:
        # print('last_write_count_cumul : ' + str(write_count_cumul))
        # print('last_like_count_cumul : ' + str(like_count_cumul))
        # print('last_retwitt_count_cumul : ' + str(retwitt_count_cumul))
        if (worksheet_data_last['게시물 누적수(D)'] == write_count_cumul and
            worksheet_data_last['좋아요 누적수(D)'] == like_count_cumul and
            worksheet_data_last['리트윗 누적수(D)'] == retwitt_count_cumul and
            worksheet_data_last['좋아요 발생'] == like_count_cumul_prev - last_row['좋아요 누적수(D)'] and
            worksheet_data_last['리트윗 발생'] == retwitt_count_cumul_prev - last_row['리트윗 누적수(D)']):
            # print("same")
            pass
        else:
            # print("diff")
            worksheet.append_row([
                                  datetime.strftime(now_time, '%Y-%m-%d %H')
                                , datetime.strftime(now_time, '%Y-%m-%d')
                                , datetime.strftime(now_time, '%H')
                                , 'normal'
                                , 0
                                , 0
                                , 0
                                , write_count_cumul if datetime.strftime(now_time, '%Y-%m-%d') == worksheet_data_last['게시일자'] else 0
                                , like_count_cumul if datetime.strftime(now_time, '%Y-%m-%d') == worksheet_data_last['게시일자'] else 0
                                , retwitt_count_cumul if datetime.strftime(now_time, '%Y-%m-%d') == worksheet_data_last['게시일자'] else 0
                                , like_count_cumul_prev - last_row['좋아요 누적수(D)']
                                , retwitt_count_cumul_prev - last_row['리트윗 누적수(D)']
                                , "", "", "", "", "", "", ""
                                , "신규 좋아요 또는 리트윗"
                                ])

    logger.info('스프레드시트 작성 종료')

    # 메일 발송
    send_email_result = send_email.send_email(constant.C_ADMIN_MAIL_ADDRESS, logfile_path)

    logger.info(f'메일 발송 결과 : {send_email_result}')

if __name__ == '__main__':

    # 현재일시
    now_time = datetime.now()

    # 로그
    logger = logging.getLogger("mainLog")
    logger.setLevel(logging.INFO)
    loggerHandler = logging.StreamHandler()

    formatter = logging.Formatter('%(asctime)s|%(name)s|%(levelname)s:%(message)s')
    loggerHandler.setFormatter(formatter)
    logger.addHandler(loggerHandler)

    # Create Handeler == 로깅한 정보가 출력되는 위치 설정
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.DEBUG)
    streamHandler.setFormatter(formatter)
    # logger.addHandler(streamHandler)

    logfile_path = '{}\log\{}.log'.format(common.resource_path(''), datetime.strftime(now_time, '%y%m%d%H%M%S'))
    # logfile_path = '{}\log\{}.log'.format(constant.C_ROOT_PATH, datetime.strftime(now_time, '%y%m%d%H%M%S'))

    fileHandler = logging.FileHandler(logfile_path, encoding='utf8')
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

    logger.info('----------------------------------------------------------------------------------------------------')
    logger.info("start : Search twitter")
    logger.info('----------------------------------------------------------------------------------------------------')

    # Main
    try:
        # 기본 검색어 - 해시태그 포함
        keywordsimple = '에피민트'
        keyword = f'{keywordsimple} OR #{keywordsimple}'

        # 확장 검색어 - 리트윗 제외
        keyword_ext = 'AND exclude:retweets'
        # keyword_ext = 'AND exclude:retweets AND filter:quote'

        # Full 검색키워드
        full_keyword = f'{keyword} {keyword_ext}'

        print(full_keyword)

        # 파라미터가 있는지 확인 - 없으면 기본 : '에피민트'
        if len(sys.argv) == 1:
            sys.argv.append(full_keyword)
        else:
            full_keyword = '{} OR #{} {}'.format(sys.argv[1], sys.argv[1], keyword_ext)

        # main 호출
        main(full_keyword)

    except Exception as inst:
        logger.error("error" + str(inst))

    logger.info('----------------------------------------------------------------------------------------------------')
    logger.info("end : Search twitter")
    logger.info('----------------------------------------------------------------------------------------------------')