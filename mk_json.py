import json

import openpyxl

xlsx_loc = 'C:/Users/3DONS/Desktop/group_num_name_update04.xlsx'    # 정리 xlsx 경로
create_json_loc = 'C:/Users/3DONS/Desktop/1'    # 생성할 json 파일 폴더 경로


def make_json(landmark_dict: dict, loc: str):
    with open(loc, 'w') as outfile:
        json.dump(landmark_dict, outfile)  # json 파일 생성


def open_xlsx(loc: str, sheet_name: str):
    wb = openpyxl.load_workbook(loc)
    ws = wb[sheet_name]

    key = []
    on3ds_value = []
    on3ds_landmark_num = []
    on3d_landmark_num = []
    on3d_value = []
    on3d_json = {}
    on3ds_json = {}
    start_row = 4

    for i in range(start_row, ws.max_row):    # 시작 row, 끝 row 로 key, value 값 추가
        key.append(ws.cell(i, 1).value)
        on3ds_value.append(ws.cell(i, 2).value)
        on3d_value.append(ws.cell(i, 6).value)

    for j in range(len(key) - 1):
        if key[j] == key[j + 1]:    # 뒤에 landmark name 과 같을 때 각각의 list 에 value 추가함.
            on3ds_landmark_num.append(on3ds_value[j])
            on3d_landmark_num.append(on3d_value[j])

        elif key[j] != key[j + 1]:
            on3ds_landmark_num.append(on3ds_value[j])    # 뒤에 landmark name 과 다를 때 list 에 value 추가 한 뒤 dict 로 생성 함.
            on3d_landmark_num.append(on3d_value[j])
            on3ds_json[key[j]] = on3ds_landmark_num
            on3d_json[key[j]] = on3d_landmark_num

            on3ds_landmark_num = []
            on3d_landmark_num = []

    return on3d_json, on3ds_json    # 각각의 dict 반환


on3d, on3ds = open_xlsx(xlsx_loc, '정리')
make_json(on3d, f'{create_json_loc}/on3d.json')
make_json(on3ds, f'{create_json_loc}/on3ds.json')
