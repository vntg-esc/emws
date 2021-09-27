# EMWS - Epimint Marketing Watchtower From SNS Data

## 개요
기존 Epimint 마케팅 채널 중 유의미한 실시간 데이터 집계가 용이한 Twitter를 선택, 파편화 된 SNS Data를 Python Crawling을 통해 수집, 통합 및 시각화 하여 이용자에게 Marketing Insight 도출을 보조하는 것을 지향

## 프로젝트 구성
Python 기반의 Library 사용, Twitter Standard API를 통해 Crawling 구현

- Tools : Vscode 1.59
- Language : Python 3.9.6
- Library : python-twitter (오픈소스)
    - https://python-twitter.readthedocs.io/en/latest/
    - https://github.com/bear/python-twitter

- API : twitter API Standard v1.1
    - https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet
    - https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets

- 반복 실행 : crontab (라이트 버전)

- Scripts Path : https://github.com/vntg-esc/emws

- 실행서버 : AWS EC2 Ubuntu Server 20.04 LTS (HVM), 프리티어
    - ip : 13.125.231.100

- DB : SQlite3 3.31.1
- DB Browser : DB Browser for SQLite 버전 3.12.2

## 상세내용
- 검색어
    - 기본 : '(에피민트 OR #에피민트) AND exclude:retweets’
    - 또는 실행 파라미터에 검색어 사용 가능
- 수집내용
    - 일자별, 시간별, 유저별(일반 사용자 글 - normal, 광고성 글 구분 - ads)
    - 게시물 수, 좋아요 수, 리트윗 수 집계

- 자료저장
    - 구글 스프레드 시트 파일명 : emws_data
        - 시트명 : 년월 ( 예 : 202109 )
        - https://docs.google.com/spreadsheets/d/1Z5yePPQLSJOpPxAOHWv4mTQJXxw_vUEjIFKBcqIzqA0/edit#gid=0
    - db 저장
        - 시트명 : 년월_일자별 (예 : 202109_일자별)
        - 저장폴더 : ./db/emws.db
        - Table : SNS_EPIMINT

- 수행주기 : 1시간

- 수집결과 메일 발송 
    - 관리자 계정 : hyunhee.lee@vntgcorp.com

- 실행시로그 / 이력
    - log : ./log/년월일시분초.log 생성
    - history : ./history/년월일시분초.json 생성

## 프로젝트 설정 - 실행방법
0. ubuntu 20.4 os 설치
1. 파이썬 3.9.6 설치 : https://freedeveloper.tistory.com/254
2. (필요시) 설치 파일 삭제
    ```bash
    ubuntu@ip-xxx-xx-x-xxx:/opt$ rm -rf opt/Python-3.9.6
    ubuntu@ip-xxx-xx-x-xxx:/opt$ rm -rf opt/Python-3.9.6.tgz
    ```
3. 폴더 생성
    ```bash
    ubuntu@ip-xxx-xx-x-xxx:/home$ sudo mkdir emws
    ```
4. 폴더 권한 부여
    ```bash
    ubuntu@ip-xxx-xx-x-xxx:/home$ sudo chmod -R 777 emws
    ```
5. 경로 이동
    ```bash
    ubuntu@ip-xxx-xx-x-xxx:/home$ cd emws
    ```
6. 가상환경 생성  / 활성화
    ```bash
    ubuntu@ip-xxx-xx-x-xxx:/home$ sudo python -m venv venv
    ubuntu@ip-xxx-xx-x-xxx:/home$ . venv/bin/activate

    가상환경 활성화 확인
    (venv) ubuntu@ip-xxx-xx-x-xxx:/home/emws$
    ```
7. 스크립트 받기
    - https://github.com/vntg-esc/emws.git
8. 패키지 설치
    ```bash
    (venv) ubuntu@ip-xxx-xx-x-xxx:/home/emws$ pip install python-twitter==3.5
    (venv) ubuntu@ip-xxx-xx-x-xxx:/home/emws$ pip install gspread==4.0.1
    (venv) ubuntu@ip-xxx-xx-x-xxx:/home/emws$ pip install oauth2client==4.1.3
    ```
9. 스크립트 실행 확인
    ```bash
    (venv) ubuntu@ip-xxx-xx-x-xxx:/home/emws$ python main.py
    ```
10. Crontab 설정 - 한시간마다 실행
    ```bash
    (venv) ubuntu@ip-xxx-xx-x-xxx:/home/emws$ crontab -e
    ```
    ```vi
    # 매 시간(1시간) 실행
    - 0 */1 * * * /home/emws/venv/bin/python3 /home/emws/main_db.py
    ```
11. Crontab 설정 변경시 재시작
    ```bash
    (venv) ubuntu@ip-xxx-xx-x-xxx:/home/emws$ sudo service cron restart
    ```

12. 로컬에서 서버 접속 - FTP Tool 사용 (예: Filezilla)
    - 프로토콜 : SFTP
    - 호스트 : 13.125.231.100
    - 사용자 : ubuntu
    - 키 파일 : .\aws_emws_key.pem

13. 로컬에서 서버 접속 - bash ( aws_emws_key.pem 파일이 존재하는 경로에서 실행 )
    ```bash
    $ ssh -i aws_emws_key.pem ubuntu@13.125.231.100
    ```
