import logging
from datetime import datetime

# 현재시간
now_time = datetime.today()

# logger
logger = logging.getLogger("log")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()

formatter = logging.Formatter('%(asctime)s|%(name)s|%(levelname)s:%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info(" server start")

# Create Handeler == 로깅한 정보가 출력되는 위치 설정
streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.DEBUG)
streamHandler.setFormatter(formatter)

logfile_path = "C:\GitHub\VNTG-N-ERP\emws\log\{}".format(datetime.strftime(now_time, '%y%m%d%H%M%S'))
logfile_path = "C:\GitHub\VNTG-N-ERP\emws\log"

fileHandler = logging.FileHandler(logfile_path)
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(formatter)

logger.addHandler(streamHandler)
logger.addHandler(fileHandler)