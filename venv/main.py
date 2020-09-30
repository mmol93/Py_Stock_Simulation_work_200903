import foreign_buy_top20
import company_buy_Top20
import trading_top
import pandas as pd
import load_excell
import stockCode_search
import requests
from bs4 import BeautifulSoup


# 어제 / 외국인 / 순매수 / top20 / 리스트형 / ok
ago2_foreign_buy_top20_list = foreign_buy_top20.ago2_foreign_top20_totall()

# 어제 / 기관 / 순매수 / top20 / 리스트형 / ok
ago2_company_buy_Top20_list = company_buy_Top20.ago2_company_top20_totall()

# 오늘 / 외국인 / 순매수 / top20 / 리스트형 / ok
today_foreign_buy_top20_list = foreign_buy_top20.today_foreign_top_totall()

# 오늘 / 기관 / 순매수 / top20 / 리스트형 / ok
today_company_buy_Top20_list = company_buy_Top20.today_company_top_totall()

# 오늘 / 거래량 상위 / top20 / 리스트형 / ok
today_trading_amount_top20 = trading_top.trading_top20()


# 중복되서 나오는 종목 선발하기
# 순서 : [어제 -> 오늘 -> 거래량] 이거를 외국인 / 기관별로 실시한다
# 그럼 외국인 / 기관 이렇게 2개의 리스트가 나오게된다

# 외국인의 어제 -> 오늘 종목 선정 - ok
result_foreign = [] #외국인 1차 선별 변수(어제 -> 오늘)
for ago2_foreign in ago2_foreign_buy_top20_list:
    for today_foreign in today_foreign_buy_top20_list:
        if ago2_foreign == today_foreign:
            result_foreign.append(today_foreign)

# 기관의 어제 -> 오늘 종목 선정 - ok
result_company = [] #기관 1차 선별 변수(어제 -> 오늘)
for ago2_company in ago2_company_buy_Top20_list:
    for today_company in today_company_buy_Top20_list:
        if ago2_company == today_company:
            result_company.append(today_company)


# 거래량 + 외국인 종목 비교 - ok
final_foregin_list = []
for trading_list1 in today_trading_amount_top20:
    if trading_list1 in result_foreign:
        final_foregin_list.append(trading_list1)

# 거래량 + 기관 종목 비교 - ok
final_company_list = []
for trading_list2 in today_trading_amount_top20:
    if trading_list2 in result_company:
        final_company_list.append(trading_list2)

# 아래의 print값이 실제로 없는지 확인(외국인 버전)
# print(final_foregin_list)
# print(today_trading_amount_top20)

if final_foregin_list:
    print("어제, 오늘 외국인 순매수 + 오늘 거래량 비교:",final_foregin_list)
else:
    print("외국인 순매수 - 거래량 일치하는 종목 없음")

if final_company_list:
    print("어제, 오늘 기관 순매수 + 오늘 거래량 비교:",final_company_list)
else:
    print("기관 순매수 - 거래량 일치하는 종목 없음")


# AI_List 결과까지 포함시킴

# 기록한 인공지능 리스트 가져오기
recommand_Ai_list = load_excell.AI_list #추천 종목

# 기록한 인공지능 종목 가격 가져오기
recommand_price_list = load_excell.call_recommand_price() # 추천가격

# 기록한 인공지능 종목의 코드 가져오기
recommand_Ai_code = stockCode_search.code_search() # 추천 종목의 코드들

# 각 추천 종목들 웹에서 현재가 얻어오기
url_1 = "https://finance.naver.com/item/main.nhn?code="   #네이버 주식_ 개별종목 앞 주소
i = 0 # 웹 스크랩을 위한 카운터
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"}

recommand_pre_price = [] # 추천 종목 현재가 리스트

ai_total_list = []  # 인공지능 관련 모든 종합 리스트

print("현재가  /  현재가  /  추천가")
while i < len(recommand_Ai_code): # AI 리스트에 적은 항목 횟수만큼 반복
    url = url_1 + str(recommand_Ai_code[i]) #url 앞주소 + 종목 코드
    res = requests.get(url, headers=headers)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "lxml")
    ai_today_price = soup.find("p", attrs={"class":"no_today"}).find("span", attrs={"class":"blind"})

    ai_today_price = ai_today_price.get_text()
    ai_today_price = ai_today_price.replace(",", "")    # ai_today_price에서 단위 구분 쉼표 제거
    ai_today_price = int(ai_today_price)    # 대소 구별을 위한 int형 전환

    recommand_pre_price.append(ai_today_price) # 추천 종목 현재가 리스트
    ai_total_list.append(recommand_Ai_list[i])
    ai_total_list.append(recommand_pre_price[i])
    ai_total_list.append(recommand_price_list[i])

    changing = (ai_today_price - recommand_price_list[i]) / recommand_price_list[i] * 100 # 해당 종목의 현재가 / 해당 종목의 추천가
    changing = round(changing, 2)
    # if ai_today_price > recommand_price_list[i]:
    #     ai_total_list.append("+" + str(changing) + "%")
    # else:
    #     ai_total_list.append("-" + str(changing) + "%")
    ai_total_list.append(str(changing) + "%")
    ai_total_list.append(url)
    print(ai_total_list)

    ai_total_list.clear()
    i += 1




