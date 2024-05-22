# coding : utf-8
# author : WONBEEN

import json

def read_json(filepath):
    with open(filepath, 'r', encoding = 'utf-8') as f:
        return json.load(f)
    
def save_json(save_path, data):
    with open(save_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)
        
def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        pass
    
    
def find_sheet_columns(worksheet, headers):
    """
    구글 스프레드 시트에서 첫 번째 행의 index 를 가져오기
    """
    # 첫 번째 행의 값을 가져옴
    first_row = worksheet.row_values(1)

    # 결과를 저장할 딕셔너리 초기화
    column_indices = {}

    # 각 헤더에 대해 첫 번째 행에서 열을 찾음
    for header in headers:
        if header in first_row:
            column_indices[header] = first_row.index(header) + 1  # 1부터 시작하도록 조정
        else:
            column_indices[header] = None  # 없을 경우 None

    return column_indices