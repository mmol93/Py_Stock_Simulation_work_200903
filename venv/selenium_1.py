from selenium import webdriver
from bs4 import BeautifulSoup

path = "C:/selenium/chromedriver"

options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument("disable-gpu")

driver = webdriver.Chrome("C:/selenium/chromedriver", options=options)
url = "https://finance.naver.com/sise/sise_deal_rank.nhn"
driver.implicitly_wait(3)

driver.get(url)
driver.switch_to.frame("buy")
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

data = driver.find_element_by_xpath("/html/body/div/div/div/div[1]/table[2]/tbody/tr[3]/td[1]/p").text
data2 = driver.find_element_by_xpath("/html/body/div/div/div/div[1]/table[2]/tbody/tr[3]/td[1]/p/a")


print(data)
print(data2)