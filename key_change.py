import json

json_loc = r'C:\Users\3DONS\Downloads\sample.json'  # 읽을 json 파일 경로
remake_json_loc = r'C:\Users\3DONS\Desktop\1\temp.json'  # 생성할 json 파일 경로
landMC = {0: [0.1234, 0.1234], 1: [0.1234, 0.1234], 2: [0.1234, 0.1234], 3: [-99999, -99999], 4: [0.1234, 0.1234], 5: [-99999, -99999]
    , 6: [0.1234, 0.1234], 7: [0.1234, 0.1234], 8: [0.1234, 0.1234], 9: [0.1234, 0.1234], 10: [0.1234, 0.1234], 11: [0.1234, 0.1234]
    , 12: [0.1234, 0.1234], 13: [0.1234, 0.1234], 14: [0.1234, 0.1234], 15: [0.1234, 0.1234], 16: [0.1234, 0.1234], 17: [0.1234, 0.1234]
    , 18: [0.1234, 0.1234], 19: [0.1234, 0.1234]}


def read_json(loc: str):  # json 읽기
    with open(loc, 'r') as t:
        json_data = json.load(t)

    return json_data


def make_json(landmark_dict: dict, loc: str):  # json 파일 생성
    with open(loc, 'w') as outfile:
        json.dump(landmark_dict, outfile, indent=4)  # indent 들여 쓰기?


data = read_json(json_loc)  # json 읽기
data_main_key = list(data.keys())  # 2중 dict -> 1층 key 나눔

key = list(landMC.keys())  # 입력된 dict, key, value 분리
value = list(landMC.values())

new_key = []
new_landmark = {}

for j in data_main_key:    # 2중 키값이 여러개 일때
    for i in key:  # 변경할 key 값 추가
        new_key.append(int(data[j][str(i)]))

new_landmark = dict(zip(new_key, value))  # key 값 변경한 dict 생성
make_json(new_landmark, remake_json_loc)  # json 생성
