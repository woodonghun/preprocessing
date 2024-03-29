import json
import math
import os

'''
    사용 gpu, memory, seed 주소값 등의 변동이 있는 값을 넣으면 자동을 batch 가 완성되는 코드
    on3ds,on3d landmark 학습 용
    
    json 파일 확인
    추가되는 seed 는 cuda0 - 제일 처음 생성되는 cuda 에 추가로 삽입함.
    
    on3ds detail seed [20, 30], resize seed [10, 20]
    on3d detail seed [20, 30], resize seed [10, 20], add resize {'Soft_Tissue_3' : 30} 
'''
# 사용 가능한 메모리
# 사용 가능 개수 = 메모리 / 2

cuda_dict = {'cuda0': 8,  # 각 cuda 사용 가능한 memory 입력, cuda 가 늘어날 경우 맞춰서 입력
             'cuda1': 0,
             'cuda2': 0,
             }

use_memory = 2  # train 할때 사용 하는 메모리
seed_num = 2  # 예외로 추가되는 group 의 seed 를 제외하고 공통 되는 seed 의 개수

detail_seed_list = [20, 30]  # detail, resize 에 맞는 seed 번호 입력
resize_seed_list = [10, 20]

# 추가되는 resize group 의 seed 번호 입력 기존 번호는 입력하면 안됨. group 명은 학습에 적용되는 group 명으로 정확히 입력 해야함.
# 정확히 입력되지 않으면 학습되지 않음.
add_resize_seed = {}    # {'Soft_Tissue_3' : 30}

drive_loc = 'C:'  # 드라이브 위치
change_mode = 'python train.py'  # train2.exe, python train.py 실행 하는 모드 python-exe
create_batch_folder_loc = r'D:\temp\temp'  # 배치 파일 생성 폴더 경로
python_path = 'C:/Users/3DONS/Desktop/PreShin/20211007'  # 파이썬 파일이 들어 있는 폴더 경로
on3d_s_group_json = r'C:\woo_project\preprocessing/on3ds_group_points.json'  # json 파일 경로, ( batch 파일을 적절하게 생성하기 위해서 필요)
train_log_path = r'D:\ons-538\log'  # 로그 폴더 경로
activate_env = 'tempallpk'  # 활성화 시킬 가상 환경


# 드라이브, py or exe, 가상 환경, 쿠다 번호, 쿠다 메모리 량, group point, group name, point, count, group count, point count, rest train
def cuda(drive: str, mode: str, env: str, cuda_num: int, cuda_memory: int, g_points: list, g_name: list, points: list, count: int, g_count: int, p_count: int,
         r_train: int):
    bat_train = total_train // sum_value  # 배치 하나당 train 할 개수

    for q in range(cuda_memory // use_memory):  # cuda 에서 돌릴수 있는 병렬 학습 개수
        if r_train == 0:
            bat_train = total_train // sum_value
        elif r_train != 0:
            # train 개수가 batch 파일 개수에 맞춰 항상 딱 떨어지지 않음
            # train 개수를 한개씩 늘려서 제작후 다시 하나씩 빼는 형식으로
            bat_train = total_train // sum_value + 1
            r_train -= 1
        with open(f"{create_batch_folder_loc}/cuda{cuda_num}/{q}_cuda_{cuda_num}.bat", 'a') as f:
            f.write(f'{drive}\n')
            f.write(f"cd {python_path}\n")
            f.write(f"call conda activate {env}\n")
            train_count = 0
            for w in range(bat_train):

                for n in range(seed_num):

                    if train_count == bat_train:  # 학습 개수 확인, batch 에 학습해야할 개수와 비교해서 같으면 break
                        break
                    if count == n:
                        if len(g_name) <= g_count / len(resize_seed_list):  # 그룹 개수 초과 할때 point 시작
                            # floor 내림을 사용해서 list index 정함
                            f.write(f"{mode} --tag detail --seed {detail_seed_list[n]} --cuda_id {cuda_num} --p {points[math.floor(p_count / len(detail_seed_list))]} >"
                                    f"{train_log_path}/detail/{points[math.floor(p_count / len(detail_seed_list))]}_seed_{detail_seed_list[n]}_cuda_id_{cuda_num}.txt\n")  # 한 줄
                            p_count += 1  # p_count 를 통해서 현재 진행된 point 확인, p_count/len(seed_list) 로 seed 개수 마다 1 씩 증가 하게 함. (floor 내림 함수)

                        else:
                            f.write(
                                f"{mode} --tag {g_name[math.floor(g_count / len(resize_seed_list))]} --p {g_points[math.floor(g_count / len(resize_seed_list))]} "
                                # f"{mode} --tag {g_name[math.floor(g_count / len(resize_seed_list))]}_seed_{resize_seed_list[n]} --p {g_points[math.floor(g_count / len(resize_seed_list))]} "
                                f"--seed {resize_seed_list[n]} --cuda_id {cuda_num} --resize > "
                                f"{train_log_path}/resize/{g_name[math.floor(g_count / len(resize_seed_list))]}_seed_{resize_seed_list[n]}_cuda_{cuda_num}.txt\n")  # 한 줄
                            g_count += 1
                        if n == seed_num - 1:
                            count -= seed_num - 1
                        else:
                            count += 1
                        train_count += 1

                if train_count == bat_train:
                    break
            f.write("pause")

    return g_count, p_count, count, r_train  # 결과 값을 넘겨 다음 cuda 에서 이어서 작업 하도록 함.


with open(f"{on3d_s_group_json}", "r") as file:  # on3d_s group 랜드마크, json 파일 읽기
    data = json.load(file)

group_points = list(data.values())
group_name = list(data.keys())
group_points_sum = []

for j in range(len(group_points)):  # landmark point 나열
    group_points_sum.append(' '.join(str(s) for s in group_points[j]))

points = sum(group_points, [])  # 2중 리스트 하나로 합침
points = list(set(points))  # group 에 겹치는 번호가 있기 때문에 point 는 중복 제거 위해서 set 함수 사용
total_train = (len(points) + len(group_name)) * seed_num  # 전체 학습 개수

sum_value = 0

print(f'train 총 개수 : {total_train}'
      f'\nbat 개수  ')
for i in range(len(list(cuda_dict.values()))):
    print(f'cuda{i} : {list(cuda_dict.values())[i] // use_memory} ')
    sum_value += list(cuda_dict.values())[i] // use_memory
rest_train = total_train % sum_value  # 나머지 train 개수
batch_train = total_train // sum_value  # 배치 하나당 train 개수
print(f'총 bat: : {sum_value}')
print(f'\nbat 하나당 train 개수 : {batch_train} --- 남은 train 개수 : {rest_train}')
print(f'추가 되는 train 개수 : {len(add_resize_seed)}')
os.mkdir(f'{create_batch_folder_loc}')  # main 폴더 생성
for key in cuda_dict.keys():
    os.mkdir(f'{create_batch_folder_loc}/{str(key)}')  # cuda 당 폴더 생성

group_count = 0
point_count = 0
count = 0

for j in range(len(cuda_dict)):  # cuda 개수 당 batch 에 명령어 입력 함수
    group_count, point_count, count, rest_train = cuda(drive_loc, change_mode, activate_env, j, list(cuda_dict.values())[j], group_points_sum, group_name, points, count,
                                                       group_count,
                                                       point_count, rest_train)

if list(add_resize_seed.keys()):  # 추가되는 resize seed 가 있으면 추가
    for i in range(len(add_resize_seed)):
        with open(f"{create_batch_folder_loc}/cuda0/0_cuda_0.bat", 'r') as f:
            lines = f.readlines()  # 모든 line 읽기
        lines.pop()  # pause 제거
        #
        lines.append(
            f"{change_mode} --tag {list(add_resize_seed.keys())[i]}_seed_{list(add_resize_seed.values())[i]} --p {' '.join(map(str, data[list(add_resize_seed.keys())[i]]))} "
            f"--seed {list(add_resize_seed.values())[i]} --cuda_id 0 --resize > "
            f"{train_log_path}/resize/{list(add_resize_seed.keys())[i]}_seed_{list(add_resize_seed.values())[i]}_cuda_0.txt\n")
        lines.append('pause')  # pause 추가
        with open(f"{create_batch_folder_loc}/cuda0/0_cuda_0.bat", 'w') as a:
            for line in lines:
                a.write(line)
# print(lines)

for key in cuda_dict.keys():  # 전체 batch 파일 실행 batch 파일 제작
    file_list = os.listdir(f'{create_batch_folder_loc}/{key}')
    with open(f'{create_batch_folder_loc}/start_train.bat', 'a') as y:
        for a in range(len(file_list)):
            y.write(f'start "{file_list[a]}" "{create_batch_folder_loc}/{key}/{file_list[a]}"\n')  # 띄어쓰기, 스페이스바 확인. 하나 차이로 오류발생

with open(f'{create_batch_folder_loc}/create_cache.bat', 'a') as z:  # cache 파일 제작 batch
    z.write(f"{drive_loc}\n")
    z.write(f"cd {python_path}\n")
    z.write(f"call conda activate {activate_env}\n")
    z.write(f"{change_mode} --create_cache --resize\n")
    z.write('pause')
