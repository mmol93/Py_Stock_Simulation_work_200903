import foreign_buy_top20
import company_buy_Top20
import lxml
import pandas as pd

df = pd.read_excel('Stock_excel.xlsm', header=0)[0]

df.종목코드 = df.종목코드.map('{:06d}'.format)

print(df.종목코드)