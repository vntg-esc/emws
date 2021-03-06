/*------------------------------
	작성일자 : 2021.09.15
	작성자 : 이현희
	내용 : TWITTER 수집 자료 집계
		  수집일자별 - 신규 게시글수, 좋아요수, 리트윗수
------------------------------*/
-- 트위터 수집 자료 원본
WITH C_DATA AS (
	SELECT A.CAMPAIGN
		 , DATETIME(A.COLLECT_AT, '-1 hours') AS COLLECT_DATE_FR
		 , A.COLLECT_AT  AS COLLECT_DATE_TO
		 , STRFTIME('%Y-%m-%d', DATETIME(A.COLLECT_AT, '-1 hours')) AS COLLECT_DATE
		 , STRFTIME('%Y-%m-%d %H', DATETIME(A.COLLECT_AT, '-1 hours')) AS COLLECT_HOUR
		 , A.ID
		 , A.CREATE_AT
		 , STRFTIME('%Y-%m-%d', DATETIME(A.CREATE_AT)) AS CREATE_DATE
		 , STRFTIME('%Y-%m-%d %H', DATETIME(A.CREATE_AT)) AS CREATE_HOUR
		 , A.USER_NAME
		 , A.USER_SCREEN_NAME
		 , A.TEXT
		 , A.FAVORITE_COUNT
		 , A.RETWEET_COUNT
		 
-- 		 , LAG(A.FAVORITE_COUNT, 1, 0) OVER (PARTITION BY A.ID ORDER BY A.COLLECT_AT) AS FAVORITE_COUNT_LAG
-- 		 , LEAD(A.FAVORITE_COUNT, 1, 0) OVER (PARTITION BY A.ID ORDER BY A.COLLECT_AT) AS FAVORITE_COUNT_LEAD
		 , (A.FAVORITE_COUNT - (LAG(FAVORITE_COUNT, 1, 0) OVER (PARTITION BY A.ID ORDER BY A.COLLECT_AT))) AS FAVORITE_COUNT_LAG_GAP
-- 		 , (LEAD(A.FAVORITE_COUNT, 1, 0) OVER (PARTITION BY A.ID ORDER BY A.COLLECT_AT)) - A.FAVORITE_COUNT AS FAVORITE_COUNT_LEAD_GAP

-- 		 , LAG(A.RETWEET_COUNT, 1, 0) OVER (PARTITION BY A.ID ORDER BY A.COLLECT_AT) AS RETWEET_COUNT_LAG
-- 		 , LEAD(A.RETWEET_COUNT, 1, 0) OVER (PARTITION BY A.ID ORDER BY A.COLLECT_AT) AS RETWEET_COUNT_LEAD
		 , (A.RETWEET_COUNT - (LAG(RETWEET_COUNT, 1, 0) OVER (PARTITION BY A.ID ORDER BY A.COLLECT_AT))) AS RETWEET_COUNT_LAG_GAP
-- 		 , (LEAD(A.RETWEET_COUNT, 1, 0) OVER (PARTITION BY A.ID ORDER BY A.COLLECT_AT)) - A.RETWEET_COUNT AS RETWEET_COUNT_LEAD_GAP
		 , A.HASHTAGS
		 , A.SEARCH_QUERY
		 , A.REMARK
	  FROM SNS_EPIMINT A
	 WHERE A.CAMPAIGN = 'twitter'
)
SELECT A.COLLECT_DATE
     , IFNULL(C.TOTAL_POST_COUNT, 0) AS TOTAL_POST_COUNT
	 , IFNULL(B.NEW_POST_COUNT, 0) AS NEW_POST_COUNT
	 , SUM(A.FAVORITE_COUNT_LAG_GAP) AS NEW_FAVORITE_COUNT
	 , SUM(A.RETWEET_COUNT_LAG_GAP) AS NEW_RETWEET_COUNT
  FROM C_DATA A 
       LEFT JOIN (   -- 일자별 게시글 수 집계
					SELECT A.COLLECT_DATE, COUNT(DISTINCT A.ID) AS NEW_POST_COUNT
					FROM C_DATA A
					WHERE A.COLLECT_DATE = A.CREATE_DATE
					GROUP BY A.COLLECT_DATE
				) B ON A.COLLECT_DATE = B.COLLECT_DATE
       LEFT JOIN (   -- 일자별 게시글 수 집계
					SELECT A.COLLECT_DATE, COUNT(DISTINCT A.ID) AS TOTAL_POST_COUNT
					FROM C_DATA A
					GROUP BY A.COLLECT_DATE
				) C ON A.COLLECT_DATE = C.COLLECT_DATE
GROUP BY A.COLLECT_DATE

-- SELECT ID, CREATE_AT, TEXT
--   FROM C_DATA A
--  WHERE A.COLLECT_HOUR = '2021-09-15 22'
-- --  WHERE A.COLLECT_DATE = '2021-09-15'
-- GROUP BY ID, CREATE_AT, TEXT

-- SELECT A.COLLECT_DATE, COUNT(DISTINCT A.ID) AS NEW_POST_COUNT
--   FROM C_DATA A
--  WHERE A.COLLECT_DATE = '2021-09-15'
--    AND A.COLLECT_DATE = A.CREATE_DATE
-- GROUP BY A.COLLECT_DATE

--  WHERE A.ID = '1435934488538730504'

  
-- SELECT COLLECT_DATE, SUM(FAVORITE_COUNT) AS FAV_CNT, SUM(RETWEET_COUNT) AS RET_CNT
--   FROM C_DATA
-- GROUP BY COLLECT_DATE
