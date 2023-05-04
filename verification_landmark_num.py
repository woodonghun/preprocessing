import os

import openpyxl

'''
    landmark 에 음수값이 몇개가 들어있는지 확인하는 코드
    mode 에 on3d or on3ds 입력
'''
xlsx_loc = r'./group_num_name_update04.xlsx'  # on3d, on3d_s 번호 정리한 xlsx
landmark_loc = r'D:\ons_538\538_training\train\landmarks'  # landmark 가 저장된 폴더
mode = 'on3ds'  # on3d, on3ds 모드 변경

# on3ds 용 음수, -99999 확인
# sort_landmark_num_change.py 먼저 실행
# landmark 의 개수 확인, -99999 가 없는 id 확인용
change_mode = {'on3d': 'F', 'on3ds': 'B'}
file_list = os.listdir(landmark_loc)  # landmark 폴더의 txt 파일 리스트

wb = openpyxl.load_workbook(xlsx_loc)
ws = wb['정리']

on3d_s_num = []  # on3ds landmark_num 리스트
zero_count = []  # on3ds landmark_num 에 zero 값 추가용 list
minus_file = []  # 음수가 들어간 id 목록 추가용
minus_landmark = []  # 음수가 사용된 landmark 추가용

for column in range(4, 124):  # 정리된 xlsx 에서 landmark 값 가지고 옴
    on3d_s_num.append(str(ws[f'{change_mode[mode]}{column}'].value))  # on3ds landmark xlsx 위치

on3d_s_num = list(set(on3d_s_num))  # xlsx 에서 landmark 번호 추가

for j in range(len(on3d_s_num)):
    zero_count.append([0, 0])  # dict 에 추가, count 용

count_on3d_s_landmark = dict(zip(on3d_s_num, zero_count))  # landmark dict 형식으로 해서 landmark 가 있을 때 [0,0] 에서 [1,0], 없을 때 [0,1] 식으로 카운팅

total_landmark = []  # id 읽고 저장용 list
complete_id = []
for j in range(len(file_list)):
    # print(file_list[j])
    # txt 읽고 변환
    count = 0
    with open(f"{landmark_loc}/{file_list[j]}", "r") as f:  # txt 읽기
        for line in f:  # 한줄씩 읽기
            landmark = (line.split(','))  # list 로 만듬 [landmark_number,x,y,z]
            total_landmark.append(landmark)  # landmark 에 추가 해서 최종 으로 다 모인 landmark list 만듬

    for q in range(len(total_landmark)):
        # -가 들어가고 -99999 가 아닌 경우에 음수 파일 목록에 추가함

        if '-' in total_landmark[q][1] or '-' in total_landmark[q][2] or '-' in total_landmark[q][3]:
            # [landmark_num ,-99999, -99999, -99999] 인 경우 count
            if '-99999' in total_landmark[q][1] and '-99999' in total_landmark[q][2] and '-99999' in total_landmark[q][3]:
                count_on3d_s_landmark[total_landmark[q][0]][1] += 1  # dict 형식 즉 ' landmark_num : [ 0 , 0 ] 에서 뒤에 +1
                count += 1

            elif '-99999' not in total_landmark[q][1] and '-99999' not in total_landmark[q][2] and '-99999' not in total_landmark[q][3]:
                # -가 들어간 landmark 가 2개 이상이면 목록에 계속 추가됨, 한번 추가되면 다시 추가 안되도록 함.
                if file_list[j] not in minus_file:
                    minus_file.append(file_list[j])

                if total_landmark[q][0] not in minus_landmark:
                    minus_landmark.append(total_landmark[q][0])
                # 제외 하면 음수값은 추가되지 않음
                count_on3d_s_landmark[total_landmark[q][0]][0] += 1  # dict 형식 즉 ' landmark_num : [ 0 , 0 ] 에서 앞에 +1,
                print(file_list[j], total_landmark[q])

        else:
            count_on3d_s_landmark[total_landmark[q][0]][0] += 1  # dict 형식 즉 ' landmark_num : [ 0 , 0 ] 에서 앞에 +1
    total_landmark = []

    if count == 0:  # 한번도 -99999 가 있는 파일에 진입 하지 않음
        complete_id.append(file_list[j])
print(f' landmark 가 온전한 파일 : {complete_id}')  # -99999 가 하나도 없는 파일

print('landmark, [사용된 횟수, -99999인 횟수]')
for item in sorted(count_on3d_s_landmark.items()):  # landmark_num : [ 사용된 횟수 , -99999 인 횟수 ]
    print(f'landmark_num : {item[0]}, 사용된 횟수 : {item[1][0]}, -99999인 횟수 : {item[1][1]}, 총 사용 횟수 : {item[1][0] + item[1][1]}')
print(f'음수가 들어간 파일 목록 : {minus_file} 총 개수 :{len(minus_file)}')  # 음수 파일 목록
print(f'음수가 들어간 landmark : {minus_landmark}')
