import traceback

import loggingExam
from builtins import print
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from StockException import StockException
import plotly.graph_objects as go #캔들그래프
import plotly.express as px #타임 그래프

class Contact:
    def __init__(self, company, str_startDate):
        self.company = company
        self.str_startDate = str_startDate

    def print_info(self):
        print("주식명 : ", self.company)
        print("시작날짜 : ", self.str_startDate)

#코드 체크
def codeCheck(company):
    stock_code = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]
    # 회사명과 종목코드만을 사용하기 위해서 나머지는 제외
    stock_code = stock_code[['회사명', '종목코드']]
    # 회사명과 종목코드를 영어로
    stock_code = stock_code.rename(columns={'회사명': 'company', '종목코드': 'code'})
    # 종목코드를 6자리로 고정
    stock_code.code = stock_code.code.map('{:06d}'.format)

    msg_type = 'codeCheck error'
    # print(stock_code[stock_code['company'].isin([company])]['company'].head().values)

    # series 내의 데이터 분해 후 입력 회사값과 비교
    try:
        if not stock_code[stock_code['company'].isin([company])]:
            msg = '존재하지않는 주식입니다.'
            raise StockException(msg_type, msg)
    except:
        # 존재하기에 에러 발생
        pass

    # 앞뒤 공백제거
    # series 내의 code 값의 헤더와 비교
    code = stock_code[stock_code['company'].isin([company])]['code'].head().values[0]
    #코드 확인
    print(code)

    return code

#날짜 체크
def dateCheck(str_startDate):
    logger.info('(startDate={})'.format(str_startDate))
    startDate_reg = re.compile(r'([12]\d{3})-(0\d|1[0-2])-([0-2]\d|3[01])$')
    msg_type = 'dateCheck error'

    if not startDate_reg.match(str_startDate):
        msg = "시작일을 확인해 주세요."
        raise StockException(msg_type, msg)

    startDate = datetime.strptime(str_startDate, '%Y-%m-%d')
    nowDate = datetime.today()
    if startDate.date() > nowDate.date():
        msg = "시작일이 미래입니다."
        raise StockException(msg_type, msg)

    print(startDate)

    return startDate



#실행
def start():
    logger.info('[start]\n')

    try:
        #주식, 취득일 입력받기
        # company, str_startDate = input("주식명, 시작날짜(예시: 삼성전자, 0000-00-00) : ").strip(',')
        company = input("주식명 : ")
        str_startDate = input("시작날짜 : ")
        print(company, str_startDate)

        code = codeCheck(company)
        startDate = dateCheck(str_startDate)


        url = 'https://finance.naver.com/item/sise_day.naver?code=' + code
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
        req = requests.get(url, headers=header)
        soup = BeautifulSoup(req.text, 'html.parser')
        # 페이지 지정 (복수)
        df = pd.DataFrame()

        # 첫 페이지를 파싱하여 전체 페이지 수 계산
        if soup.select_one('td.pgRR'):
            last_page = int(soup.select_one('td.pgRR').a['href'].split('=')[-1])
        else:
            #신규 상장등 아직 페이지가 1이 안넘는 경우 (ex:LG에너지솔루션)
            last_page = 1

        # 모든 페이지 정보 데이터 프레임 생성
        for page in range(1, last_page + 1):
            req = requests.get(f'{url}&page={page}', headers=header)
            df = pd.concat([df, pd.read_html(req.text, encoding='euc-kr')[0]], ignore_index=True)

        # 결측값 제거
        df = df.dropna()
        # 인덱스 재 배열
        df.reset_index(drop=True, inplace=True)
        # print(df)

        # 한글로 된 컬럼명을 영어로 바꿔줌
        df = df.rename(columns={'날짜': 'date', '종가': 'close', '전일비': 'diff', '시가': 'open', '고가': 'high', '저가': 'low',
                                '거래량': 'volume'})
        # 데이터의 타입을 int형으로 바꿔줌
        df[['close', 'diff', 'open', 'high', 'low', 'volume']] = df[
            ['close', 'diff', 'open', 'high', 'low', 'volume']].astype(int)
        # 컬럼명 'date'의 타입을 date로 바꿔줌
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
        # date을 기준으로 오름차순으로 변경
        df = df.sort_values(by=['date'], ascending=True)

        print(df)
        
    except StockException as se:
        logger.error(se)

    # except Exception as e:
    #     logger.error(e)



#로깅 모듈 사용하기
if __name__ == '__main__':
    logger = loggingExam.logger
    start()