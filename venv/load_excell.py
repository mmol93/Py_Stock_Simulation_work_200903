from openpyxl import load_workbook

# 불러올 엑셀 파일 설정
# data_only=True : 수식없이 값만 가져오게 설정
# 내가 저장한 AI_List 들고오기
load_wb = load_workbook("C:/Users/ijiu/Desktop/work/Git/Stock_simulation_work/venv/AI_List.xlsx", data_only=True)

# 불러올 시트 설정
load_sheet = load_wb['Sheet1']

AI_list = []  # 인공지능 종목 리스트
recomand_price = [] #인공지능 추천가

# 모든 기록한 종목 가져오기
def call_Ai_list():
    for i in range(7, 100):
        stock_name = load_sheet.cell(i, 2).value
        if stock_name == None:
            break
        AI_list.append(stock_name)

    return AI_list

# 매수 추천가 가져오기
def call_recommand_price():
    for i in range(7, 100):
        stock_price = load_sheet.cell(i, 3).value
        if stock_price == None:
            break
        recomand_price.append(stock_price)

    return recomand_price
