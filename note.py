import constant

str = "TTA AAAAAA"

# 필터 문자열이 포함되는지 확인
for filter_str in constant.C_FILTER_KEYWORD:
    if filter_str in str:
        print('포함')

# 일자별 트윗 정보 { '일자' : {'계정': {[게시글수, 좋아요수, 리트윗수]}}}
twittDaysInfo = {}
# 사용자별 트윗 정보
twittUserInfo = {}
# 일자별 트윗 정보 상세 - 게시물수, 좋아요수
twittDetailInfo = {}

{'2021-08-30': 
    {
    'normal': 
        {'writeCnt': 6, 'likeCnt': 7, 'retwittCnt': 17}, 
    'sell_coupons': 
        {'writeCnt': 3, 'likeCnt': 0, 'retwittCnt': 713}
    }
}

twittDetailInfo1 = {'writeCnt': 1, 'likeCnt': 1, 'retwittCnt': 1}
twittUserInfo['normal'] = twittDetailInfo1
twittDaysInfo['2021-08-30'] = twittUserInfo

twittDetailInfo2 = {'writeCnt': 11, 'likeCnt': 11, 'retwittCnt': 11}
twittUserInfo['sell_coupons'] = twittDetailInfo2
twittDaysInfo['2021-08-30'] = twittUserInfo

twittDetailInfo1['writeCnt'] += 1

print(twittDaysInfo)

print(twittUserInfo)

print('hoursDic--------------------')
hoursDic = {}

for i in range(0, 24, 1):
    hoursDic[i] = twittUserInfo

print(hoursDic)

