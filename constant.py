# 필터 문자열 : status.user.name에 해당 문자열이 포함되어 있으면 user_type을'ads'로 분류
C_FILTER_KEYWORD = [
    'TTA',
    'epimint',
    'EPIMINT',
]

# 프로젝트 절대경로
C_ROOT_PATH = 'C:\GitHub\VNTG-N-ERP\emws'

# 관리자 메일 주소
C_ADMIN_MAIL_ADDRESS = 'hyunhee.lee@vntgcorp.com'

# 수집 구글 스프레드시트 TITLE
C_SPREADSHEET_TITLE1 = ['수집일시','게시일자','시간(24시)','채널','게시물 수','좋아요 수','리트윗 수','게시물 누적수(D)','좋아요 누적수(D)','리트윗 누적수(D)','좋아요 발생','리트윗 발생','D+1 L&R','D+2 L&R','D+3 L&R','D+4 L&R','D+5 L&R','D+6 L&R','D+7 L&R','비고']
C_SPREADSHEET_TITLE2 = ['수집일자','신규_게시글_수','신규_좋아요_수','신규_리트윗_수']

# 구글 스프레드 시트 URL
C_SPREADSHEET_URL = 'https://docs.google.com/spreadsheets/d/1Z5yePPQLSJOpPxAOHWv4mTQJXxw_vUEjIFKBcqIzqA0/edit#gid=0'

# 구글 API KEY FILE명
C_GOOGLE_API_KEY_FILENAME = 'gspread.json'