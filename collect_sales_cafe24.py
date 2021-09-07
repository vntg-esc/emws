from selenium import webdriver 
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup 
from time import time, sleep
import os
import datetime 
import json 
import re

# selenium 브라우저를 숨긴채로 작업할것인지 아닌지
# 디버그를 위해 브라우저를 숨기지 않고 작업한다.
chrome_options = webdriver.ChromeOptions()
hidden_browser = False
if hidden_browser:
    chrome_options.add_argument('headless')
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument("disable-gpu")

chrome_options.add_argument("--ignore-certificate-error")
chrome_options.add_argument("--ignore-ssl-errors")
# chaptcha
# chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    
capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"

# SSL 오류 해제 - handshake failed; returned -1, SSL error code 1, net_error -218
# capa= webdriver.DesiredCapabilities.CHROME.copy()
capa['acceptInsecureCerts']= True
capa['acceptSslCerts']= True

driver = webdriver.Chrome(executable_path='./webdriver/chromedriver.exe', 
                        options=chrome_options,
                        desired_capabilities=capa)

# 특정 개체를 로딩 될때까지 대기하기 위해 필요하다
wait = WebDriverWait(driver, 20)

# 카페24 로그인
driver.get('https://eclogin.cafe24.com/Shop/')
# driver.get('https://eclogin.cafe24.com/Shop/?url=Init&login_mode=2&is_multi=F')

# id 입력 input이 로딩될대까지 기다린후 id와 password 입력
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mall_id')))

#부운영자 클릭
driver.find_element_by_css_selector('#contents > div > div.mTab.eTab > ul > li:nth-child(2) > a').click()

# id 입력 input이 로딩될대까지 기다린후 id와 password 입력
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#userid')))

driver.execute_script('''
document.getElementById('mall_id').value = 'episcoop';
document.getElementById('userid').value = 'looker';
document.getElementById('userpasswd').value = 'vntg0601@';
''')
# driver.execute_script('''
# document.getElementById('mall_id').value = 'ausiestory';
# document.getElementById('userpasswd').value = 'xxx';
# ''')

# id 입력 input이 로딩될대까지 기다린후 id와 password 입력
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#frm_user > div > div.mRecaptcha > div')))

# Chatpcha v2 - 로봇이 아닙니다.
# driver.find_element_by_css_selector('#recaptcha-anchor > div.recaptcha-checkbox-border').click()
driver.find_element_by_css_selector('#frm_user > div > div.mRecaptcha > div').click()
# wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#frm_user > div > div.mRecaptcha > div"))).click()

# driver.find_element_by_css_selector('#tabAdmin > div > fieldset > p.gButton > a').click()
driver.find_element_by_css_selector('#frm_user > div > div.mButton > button').click()

# cafe24 상위 메뉴가 로딩될때까지 기다린후 
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#header > div > div.head > h1 > a > img'))) 

# 일별 매출 조회 페이지로 이동
driver.get('https://episcoop.cafe24.com/disp/admin/shop1/report/DailyList')
# driver.get('https://ausiestory.cafe24.com/disp/admin/shop1/report/DailyList')

wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#content > div.headingArea > div.mTitle > h1'))) 



# # 자세히보기 체크박스 클릭
# driver.find_element_by_id('sReportGabView').click()

# sleep(1)
# # 기간설정 input이 로드 될때까지 기다린후 
# wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#pr_start_date'))) 

# sleep(1)
# # 매출 데이터를 수집할 기간을 지정
# start_date = datetime.datetime(2020, 1, 1)
# end_edate = datetime.datetime(2020,12, 15) 
# start_date_str = start_date.strftime('%Y-%m-%d')
# end_edate_str = end_edate.strftime('%Y-%m-%d')

# # 기간설정과 
# driver.execute_script('''
# document.getElementById('pr_start_date').setAttribute('value', '{}');
# document.getElementById('pr_end_date').setAttribute('value', '{}');

# document.querySelector('select#rows option[value="100"]').setAttribute('value', 500);
# '''.format(start_date_str, end_edate_str))

# driver.find_element_by_css_selector('select#rows option[value="500"]').click()

# wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.mBoard.gScroll > table'))) 
# sleep(1)

# # 데이터 테이블 태그를 빠르게 파싱하기 위해 BeautifulSoup을 사용한다.
# table_tag = driver.find_element_by_css_selector('.mBoard.gScroll > table')
# soup = BeautifulSoup(table_tag.get_attribute('outerHTML'), 'lxml')
# row_li = []
# for tr in soup.select('tbody > tr'):
#     td_li = tr.select('td')
#     row = {
#         "date" : td_li[0].text,
#         "주문수" : td_li[1].text,
#         "품목수" : td_li[2].text,
#         "상품구매금액" : td_li[3].text,
#         "배송비" : td_li[4].text,
#         "할인" : td_li[5].text,
#         "쿠폰" : td_li[6].text,
#         "실제결제금액" : td_li[7].text,
#         "적립금" : td_li[8].text,
#         "예치금" : td_li[9].text,
#         "네이버포인트" : td_li[10].text,
#         "결제합계" : td_li[11].text,
#     }
#     row_li.append(row)
    
# print( len(row_li))

# # 수집된 데이터를 확인해본다. 잘 수집되었다.
# rdf = pd.DataFrame(row_li)
# driver.quit()