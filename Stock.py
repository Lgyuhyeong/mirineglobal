import requests
import pandas as pd
#간편하게 그래프를 만들고 변화를 줄 수 있음
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from datetime import datetime


# naver https://finance.naver.com/item/sise_day.naver?code="종목코드"&page="페이지번호"

#해당 링크는 한국거래소에서 상장법인목록을 엑셀로 다운로드하는 링크
#다운로드와 동시에 Pandas에 excel 파일이 load가 되는 구조
stock_code = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]
#print(stock_code.head())

#회사명과 종목코드만을 사용하기 위해서 나머지는 제외
stock_code = stock_code[['회사명', '종목코드']]

#회사명과 종목코드를 영어로
stock_code = stock_code.rename(columns={'회사명':'company', '종목코드':'code'})
#print(stock_code.head())

#종목코드를 6자리로 고정
stock_code.code = stock_code.code.map('{:06d}'.format)
#print(stock_code.head())


#주식 일별 시세 url 가져오기
company = '삼성전자'
#앞뒤 공백제거
code = stock_code[stock_code.company == company].code.values[0].strip()

#페이지 지정 (단수)
# page = 1
# url = 'https://finance.naver.com/item/sise_day.naver?code={code}'.format(code=code)
# url = '{url}&page={page}'.format(url=url, page=page)
#print(url)
# #header를 user-agent 값
# header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
# res = requests.get(url, headers=header)
# df = pd.read_html(res.text, header=0)[0]

#페이지 지정 (복수)
df = pd.DataFrame()
for page in range(1, 20):
    url = 'https://finance.naver.com/item/sise_day.naver?code={code}'.format(code=code)
    url = '{url}&page={page}'.format(url=url, page=page)
    print(url)

#결측값 제거
df = df.dropna()
# 한글로 된 컬럼명을 영어로 바꿔줌
df = df.rename(columns= {'날짜': 'date', '종가': 'close', '전일비': 'diff', '시가': 'open', '고가': 'high', '저가': 'low', '거래량': 'volume'})
# 데이터의 타입을 int형으로 바꿔줌
df[['close', 'diff', 'open', 'high', 'low', 'volume']] = df[['close', 'diff', 'open', 'high', 'low', 'volume']].astype(int)
# 컬럼명 'date'의 타입을 date로 바꿔줌
df['date'] = pd.to_datetime(df['date'])
#date을 기준으로 오름차순으로 변경
df = df.sort_values(by=['date'], ascending=True)

fig = go.Figure(data=[go.Candlestick(x=df['date'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'])])

fig.show()

"""
#그래프 설정
plt.plot(df['date'], df['close'])
#가로
plt.xlabel('date', loc='right')
#세로
plt.ylabel('close', loc='top')
#눈금 스타일 지정하기
plt.grid(True)
plt.tick_params(axis='x')
plt.show()
"""
