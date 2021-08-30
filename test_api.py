import base64
import secrets

# b64 encoded 형태로 만드는 과정 
key_secret = '{}:{}'.format(secrets.TWITTER_CONSUMER_KEY, secrets.TWITTER_CONSUMER_SECRET).encode('ascii')
b64_encoded_key = base64.b64encode(key_secret)
b64_encoded_key = b64_encoded_key.decode('ascii')

import requests

# request에 필요한 url 만들기
base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)

# HEADER 구성하기
auth_headers = {
    'Authorization': 'Basic {}'.format(b64_encoded_key),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}

# Authentication Data section 만들기
auth_data = {
    'grant_type': 'client_credentials'
}

# POST request를 보내서 status 확인!
auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
print(auth_resp.status_code)

# Bearer token 정의하기
access_token = auth_resp.json()['access_token']

# Search HEADER 구성하기
search_headers = {
    'Authorization': 'Bearer {}'.format(access_token)
}

# SEARCH TWEET
# Maximum number of tweets returned from a single token is 18,000 

search_params = {
    'q':'에피민트',
    'count':1, # 디폴트 값은 15이며, 최대 100까지 지정 가능
    'result_type': 'recent', # 'mixed' or 'popular' 로도 지정 가능
    'retryonratelimit':True, # rate limit에 도달했을 때 자동으로 다시 trial
}

search_url = '{}1.1/search/tweets.json'.format(base_url)
search_resp = requests.get(
    search_url, headers=search_headers, 
    params=search_params
)


# print(type(search_resp))
# data = json.loads(search_resp.text)

print(search_resp.content.decode('utf-8'))



# rate limit URL
url = 'https://api.twitter.com/1.1/application/rate_limit_status.json'
search_resp = requests.get(url, headers=search_headers)

import json

# 확인하기
print(json.loads(search_resp.content)['resources']['search'])