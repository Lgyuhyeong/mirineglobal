import requests
import pandas as pd

# naver https://finance.naver.com/item/sise_day.naver?code="종목코드"&page="페이지번호"

#해당 링크는 한국거래소에서 상장법인목록을 엑셀로 다운로드하는 링크
#다운로드와 동시에 Pandas에 excel 파일이 load가 되는 구조
stock_code = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]
#stock_code.head()

#회사명과 종목코드만을 사용하기 위해서 나머지는 제외
stock_code = stock_code[['회사명', '종목코드']]

#회사명과 종목코드를 영어로
stock_code = stock_code.rename(columns={'회사명':'company', '종목코드':'code'})
#stock_code.head()

#종목코드를 6자리로 고정
stock_code.code = stock_code.code.map('{:06d}'.format)


#주식 일별 시세 url 가져오기
company = '삼성전자'
#앞뒤 공백제거
code = stock_code[stock_code.company == company].code.values[0].strip()
#페이지 지정
page = 1
url = 'https://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)
url = '{url}&page={page}'.format(url=url, page=page)
print(url)
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
res = requests.get(url, headers=header)
df = pd.read_html(res.text, header=0)[0]
df.head()

