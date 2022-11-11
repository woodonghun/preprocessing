import os


def compare(loc_1: str, loc_2: str):
    loc1_list = os.listdir(loc_1)
    loc1_only_name_list = []
    for i in loc1_list:
        loc1_only_name_list.append(i.split('.')[0])
    loc2_list = os.listdir(loc_2)

    sym_diff = list(set(loc1_only_name_list) ^ set(loc2_list))  # 대칭 차집합 교집합 뺀 나머지

    return sym_diff


def mk_list(loc_1: str, loc: str):
    loc1_list = os.listdir(loc_1)
    loc1_only_name_list = []
    for i in loc1_list:
        loc1_only_name_list.append(i.split('.')[0])

    for j in loc1_only_name_list:
        with open(f'{loc}/list.txt', 'a') as f:
            f.write(f'{j},{j}\n')


sym = compare(r'D:\538ons\ONS_file', r'\\192.168.0.42\share\temp\volume_template_input_label\input')
print(sym)

mk_list(r'D:\538ons\ONS_file', r'C:\Users\3DONS\Desktop')
