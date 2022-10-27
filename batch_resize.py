import json
import math
import os

# 사용 가능한 메모리
# 사용 가능 개수 = 메모리 / 2
cuda0_memory = 20    # 사용 가능한 메모리 작성
cuda1_memory = 0
cuda2_memory = 0

use_memory = 2     # train 할때 사용 하는 메모리
seed_num = 2    # 시드 개수

drive_loc = 'C:'    # 드라이브 위치
change_mode = 'python train.py'    # train2.exe, python train.py 실행 하는 모드 python-exe
create_batch_folder_loc = 'C:/Users/3DONS/Desktop/temp_batch_on3ds'    # 배치 파일 생성 경로
python_path = 'C:/Users/3DONS/Desktop/PreShin/20211007'    # 파이썬 경로
on3d_s_group_json = 'C:/Users/3DONS/Desktop/on3ds_group_points.json'    # json 파일 경로, ( batch 파일을 적절하게 생성하기 위해서 필요)
train_log_path = 'C:/Users/3DONS/Desktop'    # 로그 경로
activate_env = 'tempallpk'    # 활성화 시킬 가상 환경


def cuda(drive_loc: str, change_mode: str, activate_env: str, cuda_number: int, cuda_memory: int, group_points: list, group_name: list, points: list, count: int, group_count: int, point_count: int, rest_train: int):
    batch_train = total_train // (cuda0_bat+cuda1_bat+cuda2_bat)

    for i in range(cuda_memory // use_memory):    # cuda 에서 돌릴수 있는 병렬 학습 개수
        if rest_train == 0:
            batch_train = total_train // (cuda0_bat+cuda1_bat+cuda2_bat)
        elif rest_train != 0:
            # train 개수가 항상 딱 떨어지지 않음
            # train 개수를 한개씩 늘려서 제작후 다시 하나씩 빼는 형식으로
            batch_train = total_train // (cuda0_bat+cuda1_bat+cuda2_bat) +1
            rest_train -= 1
        with open(f"{create_batch_folder_loc}/cuda{cuda_number}/{i}_cuda_{cuda_number}.bat", 'a') as f:
            f.write(f'{drive_loc}\n')
            f.write(f"cd {python_path}\n")
            f.write(f"call conda activate {activate_env}\n")
            for j in range(batch_train):

                # seed 를 count 로 확인. 현재 seed 가 2개일 때만 제작이 되서 3개 이상일 떄 자동화 제작 해야함.
                # point count, group count 의 개수 증가를 [count/ (seed 개수)] 로 하고 floor 내림 사용해서 제작 하면 가능 할듯.
                # count 도 하나 더 늘리면 가능?
                if count == 0:
                    if len(group_name) <= group_count:    # 그룹 개수 초과 할때 point 시작
                        f.write(f"{change_mode} --tag detail --seed 10 --cuda_id {cuda_number} --p {points[math.floor(point_count)]} >"
                                f"{train_log_path}/detail/{points[math.floor(point_count)]}_seed_10_cuda_id_{cuda_number}.txt\n")    # floor 내림을 사용해서 list index 정함
                        point_count += 0.5
                    else:
                        f.write(
                            f"{change_mode} --tag {group_name[math.floor(group_count)]}_seed_10 --p {group_points[math.floor(group_count)]} --seed 10 --cuda_id {cuda_number} --resize > "
                            f"{train_log_path}/resize/{group_name[math.floor(group_count)]}_seed_10_cuda_{cuda_number}.txt\n")
                        group_count += 0.5
                    count += 1
                elif count == 1:
                    if len(group_name) <= group_count:
                        f.write(f"{change_mode} --tag detail --seed 20 --cuda_id {cuda_number} --p {points[math.floor(point_count)]} >"
                                f"{train_log_path}/detail/{points[math.floor(point_count)]}_seed_20_cuda_id_{cuda_number}.txt\n")
                        point_count += 0.5
                    else:
                        f.write(
                            f"{change_mode} --tag {group_name[math.floor(group_count)]}_seed_20 --p {group_points[math.floor(group_count)]} --seed 20 --cuda_id {cuda_number} --resize > "
                            f"{train_log_path}/resize/{group_name[math.floor(group_count)]}_seed_20_cuda_{cuda_number}.txt\n")
                        group_count += 0.5
                    count -= 1
            f.write("pause")

    return group_count, point_count, count, rest_train    # 결과 값을 넘겨 다음 cuda 에서 이어서 작업 하도록 함.


with open(f"{on3d_s_group_json}", "r") as file:    # on3d_s group 랜드마크, json 파일 읽기
    data = json.load(file)

group_points = list(data.values())
group_name = list(data.keys())
group_points_sum = []

for j in range(len(group_points)):    # landmark point 나열
    group_points_sum.append(' '.join(str(s) for s in group_points[j]))

points = sum(group_points, [])    # 2중 리스트 하나로 합침
points = list(set(points))    # group 에 겹치는 번호가 있기 때문에 point 는 중복 제거 위해서 set 함수 사용


cuda0_bat = cuda0_memory // use_memory
cuda1_bat = cuda1_memory // use_memory
cuda2_bat = cuda2_memory // use_memory
total_train = (len(points) + len(group_name)) * seed_num
rest_train = total_train%(cuda0_bat+cuda1_bat+cuda2_bat)    # 남은 train 개수

print(f'train 총 개수 : {total_train}'
      f'\nbat 개수 = cuda0 : {cuda0_bat} cuda1 : {cuda1_bat} cuda2 : {cuda2_bat} 총 bat: : {cuda0_bat+cuda1_bat+cuda2_bat}'
      f'\nbat 하나당 train 개수 : {total_train//(cuda0_bat+cuda1_bat+cuda2_bat)} --- 남은 train 개수 : {total_train%(cuda0_bat+cuda1_bat+cuda2_bat)}')

os.mkdir(f'{create_batch_folder_loc}')
os.mkdir(f'{create_batch_folder_loc}/cuda0')
os.mkdir(f'{create_batch_folder_loc}/cuda1')
os.mkdir(f'{create_batch_folder_loc}/cuda2')

group_count = 0
point_count = 0
count = 0

group_count, point_count, count, rest_train = cuda(drive_loc, change_mode, activate_env, 0, cuda0_memory, group_points_sum, group_name, points, count, group_count, point_count,rest_train)    # cuda0
group_count, point_count, count, rest_train = cuda(drive_loc, change_mode, activate_env, 1, cuda1_memory, group_points_sum, group_name, points, count, group_count, point_count,rest_train)    # cuda1
group_count, point_count, count, rest_train = cuda(drive_loc, change_mode, activate_env, 2, cuda2_memory, group_points_sum, group_name, points, count, group_count, point_count,rest_train)    # cuda2

file_list0 = os.listdir(f'{create_batch_folder_loc}/cuda0')
file_list1 = os.listdir(f'{create_batch_folder_loc}/cuda1')
file_list2 = os.listdir(f'{create_batch_folder_loc}/cuda2')
total_file_list = file_list0+file_list1+file_list2

with open(f'{create_batch_folder_loc}/start_train.bat','a') as y:
    for a in range(len(file_list0)):
        y.write(f'start "{file_list0[a]}" "{create_batch_folder_loc}/cuda0/{file_list0[a]}"\n')    # 띄어쓰기, 스페이스바 확인. 하나 차이로 오류발생
    for b in range(len(file_list1)):
        y.write(f'start "{file_list1[b]}" "{create_batch_folder_loc}/cuda1/{file_list1[b]}"\n')
    for c in range(len(file_list2)):
        y.write(f'start "{file_list2[c]}" "{create_batch_folder_loc}/cuda2/{file_list2[c]}"\n')

with open(f'{create_batch_folder_loc}/create_cache.bat','a') as z:     # cache 파일 제작 batch
    z.write(f"{drive_loc}\n")
    z.write(f"cd {python_path}\n")
    z.write(f"call conda activate {activate_env}\n")
    z.write(f"{change_mode} --create_cache --resize\n")
    z.write('pause')