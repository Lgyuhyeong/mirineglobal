import logging
from datetime import datetime
import os

#로그 생성
logger = logging.getLogger()

#로그의 출력 기준 설정 (DEBUG < INFO < WARNING < ERROR < CRITICAL)
logger.setLevel(logging.INFO)

#로그 출력 형식
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#로그 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

#로그를 파일에 출력 설정
date = datetime.now().strftime('%Y-%m-%d')
#디렉토리 생성
directory = './로그모음/'
os.makedirs(directory, exist_ok=True)
#로그 파일 저장
file_handler = logging.FileHandler(directory + '{date}.log'.format(date=date))
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

#깃허브 에러는 왜;;
"""
#로그 확인용
for i in range(10):
    logger.info(f'{i}번째 방문입니다.')
"""