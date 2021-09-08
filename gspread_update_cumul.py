# 구글 스프레드시트
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import common
from datetime import datetime, timedelta

now_time = datetime.today()

"""
구글스프레드시트 저장

- 추가된 필드로 인한 기존데이터 갱신 : 게시물 누적수(D), 좋아요 누적수(D), 리트윗 누적수(D)
"""
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
# worksheetName = datetime.strftime(now_time, '%Y%m')
worksheetName = f'{now_time.year}{str(now_time.month).zfill(2)}의 사본'

# 시트 선택하기
worksheet = doc.worksheet(worksheetName)

# 시트 자료 가져오기
worksheet_datas = worksheet.get_all_records()

prev_post_date = '1111-01-01'
day_count = 0
write_count_cumul = 0
like_count_cumul = 0
retwitt_count_cumul = 0

# worksheet.update('H25:J25', (10, 20, 30))

for worksheet_data in worksheet_datas:

    # if worksheet_data['게시일자'] >= '2021-09-01':

    day_count = day_count + 1 if prev_post_date == worksheet_data['게시일자'] else 0    
    prev_post_date = worksheet_data['게시일자']
    curr_hour = worksheet_data['시간(24시)']
    rowCnt = worksheet_datas.index(worksheet_data) + 2


    if day_count == 0:
        # 일자의 첫번째 시간 : 시점과 동일
        write_count_cumul = worksheet_data['게시물 수']
        like_count_cumul = worksheet_data['좋아요 수']
        retwitt_count_cumul = worksheet_data['리트윗 수']
    else:
        # 일자의 두번째 이상 시간 : 누적
        write_count_cumul += worksheet_data['게시물 수']
        like_count_cumul += worksheet_data['좋아요 수']
        retwitt_count_cumul += worksheet_data['리트윗 수']

    print(f'일자개수 {str(day_count)}, 이전일자 : {prev_post_date} 시간 : {curr_hour} | {write_count_cumul} {like_count_cumul} {retwitt_count_cumul}')

    # 여러셀 업데이트
    cell_list = worksheet.range('H{}:J{}'.format(rowCnt, rowCnt))

    cell_values = [write_count_cumul, like_count_cumul, retwitt_count_cumul]

    for i, val in enumerate(cell_values):
        cell_list[i].value = val

    worksheet.update_cells(cell_list)

    # # 한 셀씩 업데이트
    # worksheet.update_acell(f'H{rowCnt}', write_count_cumul)
    # worksheet.update_acell(f'I{rowCnt}', like_count_cumul)
    # worksheet.update_acell(f'J{rowCnt}', retwitt_count_cumul)



    # print(worksheet_data['게시일자'])
    # print(worksheet_data['시간(24시)'])

    # print(worksheet_data['게시물 수'])
    # print(worksheet_data['좋아요 수'])
    # print(worksheet_data['리트윗 수'])

    # print(worksheet_data['게시물 누적수(D)'])
    # print('게시물 누적수(D) 공백에 더하기')
    # print(worksheet_data['게시물 누적수(D)'] + 1)
    # print(worksheet_data['좋아요 누적수(D)'])
    # print(worksheet_data['리트윗 누적수(D)'])


