import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
'https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive',
]

# scope = [
# 'https://spreadsheets.google.com/auth/spreadsheets',
# 'https://www.googleapis.com/auth/drive',
# ]

json_file_name = 'gspread.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
gc = gspread.authorize(credentials)


spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1Z5yePPQLSJOpPxAOHWv4mTQJXxw_vUEjIFKBcqIzqA0/edit#gid=0'

# 스프레스시트 문서 가져오기 
doc = gc.open_by_url(spreadsheet_url)

# 시트 선택하기
worksheet = doc.worksheet('시트1')

# 1개 셀 읽기
cell_data = worksheet.acell('A1').value
print(cell_data)

# 행 데이터 읽기
row_data = worksheet.row_values(1)
print(row_data)

# # 열 데이터 읽기
# column_data = worksheet.col_values(1)
# print(column_data)

# # 특정범위 읽기
# range_list = worksheet.range('A1:D2')
# for cell in range_list:
#     print(cell.value)


# # 특정 셀 쓰기
# worksheet.update_acell('B1', 'b1 updated')

# # 행 추가1
# worksheet.append_row(['new1', 'new2', 'new3', 'new4'])

# # 행 추가2
# worksheet.insert_row(['new1', 'new2', 'new3', 'new4'], 4)

# # 크기 조정
# worksheet.resize(10,4)

# # 스프레드시트 추가
# gs = gc.create('{스프레드 시트명}')

# # 시트 추가
# worksheet = gs.add_worksheet(title='{시트명}', rows='{행 수}', cols='{열 수}')

# # 계정 공유
# gs.share('{이메일 주소}', perm_type='user', role='{권한}')
# # gs.share('{이메일 주소}', perm_type='user', role='owner')
