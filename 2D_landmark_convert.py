import json
import os

''' 
    index 번호로 구성된 2D landmark txt 구성을 2D landmark 번호로 변경 하는 코드
    2D landmark key, value 가 존재하는 json 파일이 필요
    음수값은 제거 한 뒤 새로운 파일에 txt 생성
'''

predict_label_loc = r'D:\2D_landmark\ON3DS_PreShinS2D_predict_N_label'  # label 과 predict 의 상위 폴더
json_loc = './landmarks_num_tlanslate.json'  # json파일 위치


def make_folder(loc: str, folder_name: str):    # 폴더 생성
    os.mkdir(f'{loc}/new_{folder_name}')


def list_txt(loc: str):     # txt list
    txt_list = os.listdir(loc)

    return txt_list


def convert_txt(txt_list: list, folder_name: str, data: dict):  # txt 변환 작업
    make_folder(predict_label_loc, folder_name)

    for j in range(len(txt_list)):
        with open(f"{predict_label_loc}/{folder_name}/{txt_list[j]}", "r") as f:  # txt 읽기

            for line in f:  # 한줄씩 읽기
                landmark = (line.split(','))  # list 로 만듬 [landmark_number,x,y ]

                for key, value in data['Group_A'].items():  # json 에서 읽은 변경할 2D landmark dict 를 key, value for 구동
                    if str(key) == landmark[0]:
                        landmark[0] = str(value)
                        break

                if int(landmark[0]) > 0:  # 0 이상일때만 txt에 추가함
                    result = ','.join(s for s in landmark)  # str 으로 변경
                    with open(f'{predict_label_loc}/new_{folder_name}/{txt_list[j]}', 'a') as t:  # 파일 생성
                        t.write(result)


def process(pre_lbl_loc, json_location):
    with open(json_location, 'r') as file:
        data = json.load(file)

    pre_txt_list = list_txt(f'{pre_lbl_loc}/predict')     # predict list 생성
    lbl_txt_list = list_txt(f'{pre_lbl_loc}/label')       # label list 생성

    convert_txt(pre_txt_list, 'predict', data)      # predict 변환
    convert_txt(lbl_txt_list, 'label', data)        # label 변환


process(predict_label_loc, json_loc)
