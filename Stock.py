from builtins import print
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import plotly.graph_objects as go #캔들그래프
import plotly.express as px #타임 그래프

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
# print(stock_code.head())

#주식 일별 시세 url 가져오기
company = "LG에너지솔루션"
#앞뒤 공백제거
code = stock_code[stock_code.company == company].code.values[0].strip()

#날짜 지정
def date_range(start, end):
    start = datetime.strptime(start, '%Y-%m-%d')
    end = datetime.strptime(end, '%Y-%m-%d')
    dates = [(start).strptime('%Y-%m-%d') for i in range((end-start).days+1)]
    return dates

dates = date_range("2021-01-01", "2022-02-16")

"""
#페이지 지정 (단수)
page = 1
url = 'https://finance.naver.com/item/sise_day.naver?code='+code + '&page={}'.format(page)
#print(url)
#일별시세를 가져오기 위해선 header에 user-agent 값이 필요
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
req = requests.get(url, headers=header)
df = pd.read_html(res.text, header=0)[0]
"""

#페이지 지정 (복수)
df = pd.DataFrame()
df2 = pd.DataFrame()
df3 = pd.DataFrame()

url = 'https://finance.naver.com/item/sise_day.naver?code='+code
#일별시세를 가져오기 위해선 header에 user-agent 값이 필요
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
req = requests.get(url, headers=header)
soup = BeautifulSoup(req.text, 'html.parser')

#첫 페이지를 파싱하여 전체 페이지 수 계산
if (soup.select_one('td.pgRR')):
    last_page = int(soup.select_one('td.pgRR').a['href'].split('=')[-1])
else:
    #신규 상장등 아직 페이지가 1이 안넘는 경우 (ex:LG에너지솔루션)
    last_page = 1

#모든 페이지 정보 데이터 프레임 생성
for page in range(1, last_page + 1):
    req = requests.get(f'{url}&page={page}', headers=header)
    # df = pd.concat([df, pd.read_html(req.text, encoding='euc-kr')[0]], ignore_index= True)
    df2 = df['날짜'] == dates


#결측값 제거
df = df.dropna()
#인덱스 재 배열
df.reset_index(drop= True, inplace= True)
# print(df)

# 한글로 된 컬럼명을 영어로 바꿔줌
df = df.rename(columns= {'날짜': 'date', '종가': 'close', '전일비': 'diff', '시가': 'open', '고가': 'high', '저가': 'low', '거래량': 'volume'})
# 데이터의 타입을 int형으로 바꿔줌
df[['close', 'diff', 'open', 'high', 'low', 'volume']] = df[['close', 'diff', 'open', 'high', 'low', 'volume']].astype(int)
# 컬럼명 'date'의 타입을 date로 바꿔줌
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

#csv파일 저장
df.to_csv(company+'.csv', encoding='utf-8')

#date을 기준으로 오름차순으로 변경
df = df.sort_values(by=['date'], ascending=True)

print(df)

"""
#캔들 그래프 만들기
fig = go.Figure(data=[go.Candlestick(x=df['date'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'])])
#레이아웃
fig.update_layout(
    title=company +"(종목코드 : "+ code +")",
    #가로
    xaxis_title='Date',
    #세로
    yaxis_title='Close'
)
"""


#반응형 그래프 가로는 날짜 세로는 종가
fig = px.line(df, x='date', y='close', title= "{}({})의 종가".format(company, code))
#시계열(범위 선택기 버튼)
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),#1달
            dict(count=3, label="3m", step="month", stepmode="backward"),#3달
            dict(count=6, label="6m", step="month", stepmode="backward"),#6달
            dict(count=1, label="1y", step="year", stepmode="backward"),#1년
            dict(step="all")#전체
        ])
    )
)

fig.show()
