import csv
import requests
from bs4 import BeautifulSoup
import lxml

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"}
url = "http://vip.mk.co.kr/newSt/rate/cost_up.php"  # 네이버 주식 사이트 아님(거래대금 상위를 얻기위해 바꿈)

res = requests.get(url, headers=headers)
res.raise_for_status()
soup = BeautifulSoup(res.content, "lxml")

def trading_top20():
    data_rows = soup.find("table", attrs={"class": "table_5"}).find_all("a")
    stock_name = []
    for row in data_rows:
        stock_name.append(row.get_text())   # 발견한 요소를 하나씩 텍스트 부분만 골라넣기
        if len(stock_name) > 19:    # 상위 20개만 받음
            break
    return stock_name

