from send_email import send_email
import sys, os
from datetime import datetime, timedelta
import constant
import common

# 구글 스프레드시트
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# filter_string = "TTA AAAAAA"

# # 필터 문자열이 포함되는지 확인
# for filter_str in constant.C_FILTER_KEYWORD:
#     if filter_str in filter_string:
#         print('포함')

# # 일자별 트윗 정보 { '일자' : {'계정': {[게시글수, 좋아요수, 리트윗수]}}}
# twittDaysInfo = {}
# # 사용자별 트윗 정보
# twittUserInfo = {}
# # 일자별 트윗 정보 상세 - 게시물수, 좋아요수
# twittDetailInfo = {}

# {'2021-08-30': 
#     {
#     'normal': 
#         {'writeCnt': 6, 'likeCnt': 7, 'retwittCnt': 17}, 
#     'sell_coupons': 
#         {'writeCnt': 3, 'likeCnt': 0, 'retwittCnt': 713}
#     }
# }

# twittDetailInfo1 = {'writeCnt': 1, 'likeCnt': 1, 'retwittCnt': 1}
# twittUserInfo['normal'] = twittDetailInfo1
# twittDaysInfo['2021-08-30'] = twittUserInfo

# twittDetailInfo2 = {'writeCnt': 11, 'likeCnt': 11, 'retwittCnt': 11}
# twittUserInfo['sell_coupons'] = twittDetailInfo2
# twittDaysInfo['2021-08-30'] = twittUserInfo

# twittDetailInfo1['writeCnt'] += 1

# # print(twittDaysInfo)

# # print(twittUserInfo)

# # print('hoursDic--------------------')
# hoursDic = {}

# for i in range(0, 24, 1):
#     hoursDic[i] = twittUserInfo

# # print(hoursDic)



# now = datetime.now().strftime('%Y')
now_time = datetime.today()

# print(now)
# print(now_time)

# worksheetName = datetime.strftime(now_time, '%Y%m')
# print(worksheetName)
# worksheetName = str(now_time.year) + str(now_time.month).zfill(2)
# worksheetName = f'{now_time.year}{str(now_time.month).zfill(2)}'
# print(worksheetName)


# # print('now_time.hour : ' + str(now_time.hour) + str(now_time.minute))

# nowStr = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
# # print(nowStr)

# path = "./history/{}.json".format(datetime.strftime(datetime.now(), '%y%m%d%H%M%S'))

# # print(path)

# if 'RT ' in 'RT @FROM_HW: #반민초 해시 걸고                   에피민트 광고하면서':
#     print('true')
# else:
#     print('false')

# outfile = open("./html/RESULT_MAIL_TEMPLATE.html", 'r', encoding='utf8')
# soup = outfile.read()

# # print(soup)


# test1 = '<p style="MARGIN-BOTTOM: 0px; MARGIN-TOP: 0px; LINE-HEIGHT: 150%"> PROCESS_NAME 프로세스가 수행되었습니다.</p>'
# test1 = 'PROCESS_NAME 프로세스가 수행되었습니다.'
# test1 = test1.replace("PROCESS_NAME", "test")
# # print(test1)


# data_string = 'epimint asdf'
# filterList = bool([element for element in constant.C_FILTER_KEYWORD if(element in data_string)])

# # print(filterList)


# username = 'ads' if bool(filterList) is True else 'normal'
# # print('test1 : ' + username)

# if bool(filterList):
#     username = 'ads'
# else:
#     username = 'normal'

# # print('test2 : ' + username)


# # print('{} {}'.format('에피민트', 'AND :ex'))

# # print(ord('H'))
# # print(chr(ord('H') + 1))
# # print(chr(ord('H') + 2))

# stdDateStr = '2021-09-01 17'
# # print(datetime.strptime(stdDateStr, '%Y-%m-%d %H'))
# # print(datetime.strptime(stdDateStr, '%Y-%m-%d %H') + timedelta(hours=1))
# # print(datetime.strptime(stdDateStr, '%Y-%m-%d %H') + timedelta(days=1))
# # print(datetime.strftime(datetime.strptime(stdDateStr, '%Y-%m-%d %H') + timedelta(hours=1), '%Y-%m-%d %H'))


# # print(datetime.strftime(datetime.now(), '%Y-%m-%d %H'))
# # datetime.now()
# # timedelta(hours=9)

# # print(datetime.strptime('2021-09-02', '%Y-%m-%d') + timedelta(days=1))
# # print(datetime.strptime(datetime.strftime(datetime.now(), '%Y-%m-%d'), '%Y-%m-%d'))

# # print(datetime.strftime('2021-09-02', '%Y-%m-%d'))

# colName = "H"
# stdDateStr = '2021-08-27'
# nowtime = datetime.now()
# for i in range(0, 7):
#     # print('i : {}'.format(i))
#     if (datetime.strptime(stdDateStr, '%Y-%m-%d') + timedelta(days=i+1) == 
#         datetime.strptime(datetime.strftime(nowtime, '%Y-%m-%d'), '%Y-%m-%d')):
#         # print('게시일자 + {}일이 수집일자와 동일'.format(i+1))
#         # print(chr(ord(colName) + i))
#         pass

# keyword = '에피민트'
# # 확장 검색어 - 리트윗 제외
# extword = 'AND exclude:retweets'
# # extword = 'AND exclude:retweets AND filter:quote'
# # Full 검색키워드
# fullkeyword = f'{keyword} {extword}'
# # print(fullkeyword)


# def test_kwargs(test1, **kwargs):
#     print(test1)
#     print(kwargs['keyword1234'])

# # test_kwargs('test1', keyword1234='1234')


# test_dic = {'2021-09-03': {'14': {'normal': {'write_count': 1, 'like_count': 2, 'retwitt_count': 0}}}, '2021-09-02': {'15': {'normal': {'write_count': 1, 'like_count': 1, 'retwitt_count': 0}}}, '2021-09-01': {'22': {'normal': {'write_count': 1, 'like_count': 1, 'retwitt_count': 0}}}, '2021-08-31': {'23': {'normal': {'write_count': 1, 'like_count': 1, 'retwitt_count': 0}}}, '2021-08-30': {'11': {'normal': {'write_count': 1, 'like_count': 2, 'retwitt_count': 0}}}, '2021-08-29': {'23': {'normal': {'write_count': 1, 'like_count': 1, 'retwitt_count': 0}}}, '2021-08-28': {'23': {'normal': {'write_count': 1, 'like_count': 0, 'retwitt_count': 0}}}, '2021-08-27': {'22': {'normal': {'write_count': 1, 'like_count': 2, 'retwitt_count': 0}}}, '2021-08-26': {'21': {'normal': {'write_count': 1, 'like_count': 1, 'retwitt_count': 0}}}}

# # test_nest = [testdic_key, testdic_value for testdic_key, testdic_value in test_dic.items()]

# # for testdic_key, testdic_value in test_dic.items():
# #     print(testdic_key, testdic_value)

# keywordsimple = '에피민트'
# keyword = f'{keywordsimple} OR #{keywordsimple}'

# print(keyword)


# def resource_path(relative_path):
#     """ Get absolute path to resource, works for dev and for PyInstaller"""
#     try:
#         # PyInstaller creates a temp folder and stores path in _MEIPASS
#         base_path =  sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath(".")
#     return os.path.join(base_path, relative_path)

# print(resource_path('aaa.py'))
# print(resource_path('history\{}.json'))

# filter_list = [element for element in constant.C_FILTER_KEYWORD if(element in 'EPIMINT')]
# print(filter_list)

# logfile_path = f'{constant.C_ROOT_PATH}\log\log.txt'
# logfile_path = '{}\log\log_{}.txt'.format(constant.C_ROOT_PATH, datetime.strftime(now_time, '%y%m%d%H%M%S'))

# print(logfile_path)


# logfile_path = "C:\GitHub\VNTG-N-ERP\emws\log\{}.log".format('210906170002')
# print(logfile_path)
# print(os.path.basename(logfile_path))
# # send_email('hyunhee.lee@vntgcorp.com', "C:\GitHub\VNTG-N-ERP\emws\log\{}.log".format('210906170002'))


# print(common.resource_path(''))


# import itertools

# monthly_income = [1161, 1814, 1270, 2256, 1413, 1842, 2221, 2207, 2450, 2823, 2540, 2134]
# result = list(itertools.accumulate(monthly_income))

# print(result)


# """구글스프레드시트 저장"""
# scope = [
# 'https://spreadsheets.google.com/feeds',
# 'https://www.googleapis.com/auth/drive',
# ]

# json_file_name = common.resource_path('gspread.json')
# # json_file_name = f'{constant.C_ROOT_PATH}\gspread.json'

# credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
# gc = gspread.authorize(credentials)


# spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1Z5yePPQLSJOpPxAOHWv4mTQJXxw_vUEjIFKBcqIzqA0/edit#gid=0'

# # 스프레스시트 문서 가져오기 
# doc = gc.open_by_url(spreadsheet_url)

# # 스프레드시트 문서명
# # worksheetName = datetime.strftime(now_time, '%Y%m')
# worksheetName = f'{now_time.year}{str(now_time.month).zfill(2)}의 사본'

# # 시트 선택하기
# worksheet = doc.worksheet(worksheetName)

# # 시트 자료 가져오기
# worksheet_datas = worksheet.get_all_records()

# for worksheet_data in worksheet_datas:
#     print(worksheet_data['수집일시'] )
#     print('{} {}'.format(worksheet_data['게시일자'], str(worksheet_data['시간(24시)']).zfill(2)))

# # cell_list = worksheet.range('S1:U1')

# # cell_values = [1, 2, 3]

# # for i, val in enumerate(cell_values):
# #     cell_list[i].value = val

# # worksheet.update_cells(cell_list)

# print(worksheet_datas)
# # filter_list = [element for element in constant.C_FILTER_KEYWORD if(element in status.user.name)]

# exsistsyn = [worksheet_data['게시일자'] for worksheet_data in worksheet_datas]

# print(exsistsyn)


# ['2021-09-02 15', '2021-09-02 15', '2021-09-02 15', '2021-09-02 15', '2021-09-02 15', '2021-09-02 15', '2021-09-02 15', '2021-09-02 15', '2021-09-02 15', '2021-09-02 15', '2021-09-02 15', '2021-09-02 15', '2021-09-02 15', '2021-09-02 15', '2021-09-02 15', '2021-09-02 15', '2021-09-02 15', '2021-09-02 15', '2021-09-02 15', '2021-09-02 15', '2021-09-02 15', '2021-09-02 15', '2021-09-02 15', '2021-09-02 15', '2021-09-02 15']

# test_list = ['1', '2', '3']

# test_list.insert(0, 4)

# print(test_list)


# date_str_f = '20' + '210913153747'
# print(date_str_f)
# date_date_f = datetime.strptime(date_str_f,'%Y%m%d%H%M%S')
# print(str(date_date_f.month).zfill(2))
# date_date_str_f = datetime.strftime(date_date_f,'%Y%m%d%H%M%S')
# print(date_date_str_f)

# 2021 09M 13D 15H 37m 47s


print('210914040001'[0:2])
print('210914040001.py'.replace('.py', ''))

# path = "./test/history"
# file_list = os.listdir(path)

# for file_name in file_list:
#     if file_name[8:10] == '00':
#         print('정각', file_name)
    # else:
    #     print('아님', file_name)

# print([file_name for file_name in file_list if file_name[8:10] == '00'])
# print ("file_list: {}".format(file_list))

# 현재일시
now_time = datetime.now()
file_name = datetime.strftime(now_time, '%y%m%d%H%M%S')
print(file_name)

print(common.resource_path('history{}{}.json').format(os.path.sep, file_name))