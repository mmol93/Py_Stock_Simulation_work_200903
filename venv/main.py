import foreign_buy_top20
import company_buy_Top20
import trading_top
import load_excell
import stockCode_search
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime
import os
import shutil
import time

print("실시 날짜: " + str(datetime.now().strftime("%Y/%m/%d, %H:%M")))

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
# 순서 : [어제 -> 오늘 -> 거래량] 이거를 외국인 / 기관별로 실시한다(셋 다 교집합이 되는 종목만 출력함)
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
    print("(코스피)어제, 오늘 외국인 순매수 + 오늘 거래량 비교:",final_foregin_list)
else:
    print("외국인 순매수 - 거래량 일치하는 종목 없음")

if final_company_list:
    print("(코스피)어제, 오늘 기관 순매수 + 오늘 거래량 비교:",final_company_list)
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

print("현재가  /  현재가  /  추천가  /  외국인 수급  /  기관 수급")
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

    # 숫자만 있으면 어색하니 페센트 넣기
    ai_total_list.append(str(changing) + "%")

    ## 외국인, 기관 수급 확인하기(최근 6일간)
    # 정보가 없는 주식도 있기 때문에 예외 처리를 한다
    # XPATH를 이용하여 정보를 가져와야하기 때문에 selenium을 사용한다
    xpath_counter = 0;
    xpath_num = 2;
    path = "C:/selenium/chromedriver"
    forign_buyingHistory_unit = ""

    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome("C:/selenium/chromedriver", options=options)
    driver.get(url)

    #먼저 외국인 수급 확인
    try:
        # 현재 표에 있는 외국인 기간 데이터를 모두 얻음(6일치)
        while xpath_num <= 7:
            xpath = "//*[@id='content']/div[2]/div[2]/table/tbody/tr["

            forign_buyingHistory = driver.find_element_by_xpath(
            xpath + str(xpath_num) + "]/td[3]/em").text

            # 처음(오늘날짜)에는 +, - 상관없이 카운터에 무조건 +1을 함
            # 그리고 +인지 -인지 forign_buyingHistory_unit에 기록
            # 단, 오늘 날짜에 데이터가 없을 경우 break 실시
            if xpath_counter == 0 and forign_buyingHistory[0] == "+":
                forign_buyingHistory_unit = "+"
                xpath_counter += 1
            elif xpath_counter == 0 and forign_buyingHistory[0] == "-":
                forign_buyingHistory_unit = "-"
                xpath_counter += 1

            # 최초 카운터 이후 직전에 얻은 단위(+,-)와 비교하면서 일치하면 count +1
            elif xpath_counter >= 1 and forign_buyingHistory[0] == forign_buyingHistory_unit:
                xpath_counter += 1
            else:
                forign_buyingHistory_message = "(" + str(forign_buyingHistory_unit) + str(xpath_counter) + "일간)"
                break;
            xpath_num += 1
        forign_buyingHistory_message = "("  + str(forign_buyingHistory_unit) + str(xpath_counter) + "일간)"
    except:
        forign_buyingHistory_message = "수급정보 없음"

    # 기관 수급 확인
    # 위에서 사용한 변수 초기화
    xpath_counter = 0;
    xpath_num = 2;
    company_buyingHistory_unit = ""
    try:
        # 현재 표에 있는 기관의 기간 데이터를 모두 얻음(6일치)
        while xpath_num <= 7:
            xpath = "//*[@id='content']/div[2]/div[2]/table/tbody/tr["

            company_buyingHistory = driver.find_element_by_xpath(
                xpath + str(xpath_num) + "]/td[4]/em").text

            # 처음(오늘날짜)에는 +, - 상관없이 카운터에 무조건 +1을 함
            # 그리고 +인지 -인지 forign_buyingHistory_unit에 기록
            # 단, 오늘 날짜에 데이터가 없을 경우 break 실시
            if xpath_counter == 0 and company_buyingHistory[0] == "+":
                company_buyingHistory_unit = "+"
                xpath_counter += 1
            elif xpath_counter == 0 and company_buyingHistory[0] == "-":
                company_buyingHistory_unit = "-"
                xpath_counter += 1

            # 최초 카운터 이후 직전에 얻은 단위(+,-)와 비교하면서 일치하면 count +1
            elif xpath_counter >= 1 and company_buyingHistory[0] == company_buyingHistory_unit:
                xpath_counter += 1
            else:
                company_buyingHistory_message = "(" + str(company_buyingHistory_unit) + str(xpath_counter) + "일간)"
                break;
            xpath_num += 1
        company_buyingHistory_message = "(" + str(company_buyingHistory_unit) +str(xpath_counter) + "일간)"
    except:
        company_buyingHistory_message = "수급정보 없음"

    # 해당 주식의 네이버 주식 페이지 주소도 같이 넣기
    ai_total_list.append(forign_buyingHistory_message)
    ai_total_list.append(company_buyingHistory_message)
    ai_total_list.append(url)
    print(ai_total_list)

    ai_total_list.clear()
    i += 1

## 현재 시간이 16시을 넘었을 때, AI_List.xlsx 파일을 onedrive에 저장하기
now = datetime.now()
now_hour = now.strftime("%H")
now_min = now.strftime("%M")

if (int(now_hour) >= 16):
    shutil.copyfile("C:/Users/ijiu/Desktop/work/Git/Stock_simulation_work/venv/AI_List.xlsx",
                "C:/Users/ijiu/OneDrive/AI_List.xlsx")
    print("엑셀 백업 성공")

driver.quit()

