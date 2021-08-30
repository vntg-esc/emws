import twitter

# dict[string, dic]
print('dict[string, dic]')
twittInfo = {}
twittDetailInfo = []

print(type(twittInfo))

twittDetailInfo = {'writerCnt': 1, 'likeCnt': 3, 'retwittCnt' : 0}
twittInfo['2021-08-30'] = twittDetailInfo

if twittInfo

print(twittInfo)
print(twittDetailInfo)

# twittInfo['created_at'].append('222')

# print(twittInfo)




# # twitter_consumer_key = I"qbhQ1AwYrTFEMvxEnIMQcphA"
# # twitter_consumer_secret = k"2zx7wvF610rToWkkwkxDFNNHWuLLhTHDcnDoludDREh74H3jz"  
# # twitter_access_token = q"153372335-p54Axs900ndAJKWm4cMQEytisgLWWKNJ7i4StYs"
# # twitter_access_secret = J"0DjinX48QlJ9yFz2MaR2KvN1i0pZJU7tNQOo4LfdoDyK"

# import twitter
# import datetime
# # import twitterscraper

# # tw = twitterscraper.query_tweets()
# # print(tw)

# twitter_api = twitter.Api(consumer_key=twitter_consumer_key,
#                           consumer_secret=twitter_consumer_secret, 
#                           access_token_key=twitter_access_token, 
#                           access_token_secret=twitter_access_secret)

# # # # 특정 계정의 타임라인 긁어오기 GetUserTimeline()
# # # account = "@ausiestory"
# # # statuses = twitter_api.GetUserTimeline(screen_name=account, count=200, include_rts=True, exclude_replies=False)

# # # # print(statuses)
# # # for status in statuses:
# # #     print(datetime.datetime.strptime(status.created_at,'%a %b %d %H:%M:%S +0000 %Y') + datetime.timedelta(hours=9))
# # #     print(status.text)
# # # #     print(status.text.encode('utf-8'))
# # # print(len(statuses))

# # 검색하기-1 GetSearch() 
# query = "에피민트"
# statuses = twitter_api.GetSearch(term=query, count=5)
# #     print(status.text.encode('utf-8'))
# print(type(statuses))
# print('-----------')
# for status in statuses:
#     print(type(status))
#     # print(status.id_str)
#     # print(status.user.screen_name)
#     # print(status.hashtags)
#     # print(status.favorite_count)
#     # print(datetime.datetime.strptime(status.created_at,'%a %b %d %H:%M:%S +0000 %Y') + datetime.timedelta(hours=9))
#     # print(status.text)
#     print('-----------')
# print(len(statuses))


# # # # # 검색하기-2 GetSearch() 
# # # from collections import Counter
# # # query = "#에피민트"
# # # statuses = twitter_api.GetSearch(term=query, count=100)
# # # result = []
# # # for status in statuses:
# # #     for tag in status.hashtags:
# # #         result.append(tag.text)
        
# # # Counter(result).most_common(20)


# # # statuse = twitter_api.GetFavorites(user_id='1429093943694692355')
# # # print(statuse)

