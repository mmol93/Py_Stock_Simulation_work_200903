import foreign_buy_top20
import company_buy_Top20
import pandas as pd



def match_name_code():
    ago2_foreign_top20_dict = {}
    ago2_foreign_top20_name = foreign_buy_top20.ago2_foreign_top20_totall()  # 리스트형 / 어제 / 외국인 순매수 / top20
