from openpyxl import load_workbook

# 엑셀에 있는 종목을 확인하고 그 종목의 해당 분기와 

# 불러올 엑셀 파일 설정
# data_only=True : 수식없이 값만 가져오게 설정
# 내가 저장한 AI_List 들고오기
load_wb = load_workbook("C:/Users/ijiu/Desktop/work/Git/Stock_simulation_work/venv/AI_List.xlsx", data_only=True)

# 불러올 시트 설정
load_sheet = load_wb['Sheet2']