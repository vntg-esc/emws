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

- 실행서버 : AWS EC2 Ubuntu Server 18.04 LTS (HVM), 프리티어
    - ip : 15.164.219.146

- DB : SQlite3


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

- 수행주기 : 1시간

- 수집결과 메일 발송 
    - 관리자 계정 : hyunhee.lee@vntgcorp.com

- 실행시로그 / 이력
    - log : ./log/년월일시분초.log 생성
    - history : ./history/년월일시분초.json 생성