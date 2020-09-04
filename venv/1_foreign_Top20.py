from selenium import webdriver
from bs4 import BeautifulSoup

path = "C:/selenium/chromedriver"

options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument("disable-gpu")

driver = webdriver.Chrome("C:/selenium/chromedriver", options=options)
url = "https://finance.naver.com/sise/sise_deal_rank.nhn"   #네이버 주식_외국인 순매수
driver.implicitly_wait(3)   #인터넷 로딩위해 3초 기다림

driver.get(url)
driver.switch_to.frame("buy")   # 해당 표는 iframe으로 되어있기 때문에 iframe을 로딩시켜줌
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

def foreign_top5():
    i = 0 # Top5까지 자료 가져오기 위한 카운터
    data_foreign_top5 = []
    yester_xpath1 = "/html/body/div/div/div/div[1]/table[2]/tbody/" # 어제 일자 외국인 상위매수 종목 앞 PATH

    while i < 5:    # 어제 + 1~5위 외국인 순매수
        data = driver.find_element_by_xpath(yester_xpath1 + "tr[" + str(i+3) + "]/td[1]/p").text
        print(data)
        data_foreign_top5.append(data)
        i += 1
    return data_foreign_top5


def foreign_top10():
    i = 11 # Top5까지 자료 가져오기 위한 카운터
    data_foreign_top10 = []
    yester_xpath1 = "/html/body/div/div/div/div[1]/table[2]/tbody/" # 어제 일자 외국인 상위매수 종목 앞 PATH

    while i < 16:    # 어제 + 5~10위 외국인 순매수
        data = driver.find_element_by_xpath(yester_xpath1 + "tr[" + str(i) + "]/td[1]/p").text
        print(data)
        data_foreign_top10.append(data)
        i += 1
    return data_foreign_top10

def foreign_top15():
    i = 19 # Top15까지 자료 가져오기 위한 카운터
    data_foreign_top15 = []
    yester_xpath1 = "/html/body/div/div/div/div[1]/table[2]/tbody/" # 어제 일자 외국인 상위매수 종목 앞 PATH

    while i < 24:    # 어제 + 10~15위 외국인 순매수
        data = driver.find_element_by_xpath(yester_xpath1 + "tr[" + str(i) + "]/td[1]/p").text
        print(data)
        data_foreign_top15.append(data)
        i += 1
    return data_foreign_top15

def foreign_top20():
    i = 27 # Top20까지 자료 가져오기 위한 카운터
    data_foreign_top20 = []
    yester_xpath1 = "/html/body/div/div/div/div[1]/table[2]/tbody/" # 어제 일자 외국인 상위매수 종목 앞 PATH

    while i < 32:    # 어제 + 15~20위 외국인 순매수
        data = driver.find_element_by_xpath(yester_xpath1 + "tr[" + str(i) + "]/td[1]/p").text
        print(data)
        data_foreign_top20.append(data)
        i += 1
    return data_foreign_top20

