import pandas as pd
import os
import re

''' 
    volume template label data 를 구간 별 개수를 나누어 xlsx 로 출력 하는 코드 
    data 범위를 0~127로 맞추기 위해 hts-128, sts-256 적용
'''

volume_template_label_root = r'D:\Volume Template\AUG_ON3DS_VT\valid'  # 정답 데이터 루트
xlsx_root = r'D:\Volume Template\AUG_ON3DS_VT'  # xlsx 생성 root
xlsx_name = r'valid.xlsx'  # 엑셀 명 .xlsx 붙여야함
label_range = 16  # 구간의 개수

id_list = os.listdir(volume_template_label_root)  # id list
column = ['air', 'hts', 'sts']

# id label data 생성, 숫자 제외 하고 나머지 제거
label_data = []
for i in id_list:
    id_label_data = os.listdir(fr'{volume_template_label_root}\{i}')
    for j in range(len(id_label_data)):
        id_label_data[j] = re.sub(r'[^0-9]', '', id_label_data[j])
    label_data.append(id_label_data)

df_vol_temp = pd.DataFrame(index=id_list, data=label_data, columns=column)  # dataframe 생성, list로 구성된 index, data, columns 사용
df_vol_temp = df_vol_temp.astype('int') # dataframe str => int
df_original = df_vol_temp.copy()    # 원본 보존하기 위해서 copy 사용

# 구간 통일하기 위해서 뺌.
hts = df_vol_temp['hts'].sub(128)
sts = df_vol_temp['sts'].sub(256)

# 변경한 값과 처음 데이터 바꿈
df_vol_temp['hts'] = hts
df_vol_temp['sts'] = sts

print('air, hts, sts 각각 개수 : 128')
print(f'나눌 구간 개수 : {label_range}')
print(f'128개 총 구간 개수 몫 : {128 // label_range} 나머지 : {128 % label_range}')

df_info = pd.DataFrame(index=['몫','나머지'], data=[128//label_range, 128%label_range], columns=[f'구간 : {label_range}'])

# 구간 설정
# 처음 [0], 마지막 [127]로 변경
# 마지막 개수는 많아도 더 나머지를 더 추가함
range_list = [0]
range_list_number = []
for i in range(label_range):
    range_list_number.append(i+1)
    range_list.append((i + 1) * (128 // label_range)-1)

if 128 % label_range != 0:
    range_list.append(127)
    range_list_number.append('나머지 구간')

print(range_list)

# 구간 dataframe
df_range = pd.DataFrame(data=range_list_number,columns=['구간'])

# 구간 나누기
# print(df_vol_temp['air'].value_counts(bins=range_list, sort=False))
# print(df_vol_temp['hts'].value_counts(bins=range_list, sort=False))
# print(df_vol_temp['sts'].value_counts(bins=range_list, sort=False))

# dataframe to excel
with pd.ExcelWriter(f'{xlsx_root}\{xlsx_name}') as writer:
    df_original.to_excel(writer)
    df_vol_temp.to_excel(writer, startcol=5)
    # 구간 나누기
    df_vol_temp['air'].value_counts(bins=range_list, sort=False).to_excel(writer, startcol=10)
    df_vol_temp['hts'].value_counts(bins=range_list, sort=False).to_excel(writer, startcol=12)
    df_vol_temp['sts'].value_counts(bins=range_list, sort=False).to_excel(writer, startcol=14)
    df_info.to_excel(writer, startcol=18)
    df_range.to_excel(writer,startcol=16,index=False)
