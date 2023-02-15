import os

'''
    volume template 추론 batch 생성 코드
'''

file_name = 'ON3DS_VT.exe'  # 0 AI 프로그램 실행 파일   args[0]
key = 'temp1'  # 1 프로그램 구동용 비밀키  args[1]
result_report_path = 'temp2'  # 2 결과 리포트 파일의 경로  args[2]
root_dir = ''  # 3 "/ON3DS/AI 폴더의 절대 경로"    args[3]
# mha_dir = ''  # 4 추론 할 image 파일이 있는 폴더 경로           4, 5 는 코드 내에서 추가 args 사용 안함
# mha_filename = '' # 5 추론 할 image 파일 이름 ( 파일 고유 id.mha)
model_dir = 'temp6'  # 6 pth 파일이 있는 폴더 경로    args[4]
output_path = 'temp7'  # 7 추론 한 예측 결과를 저장할 경로    args[5]
use_gpu = '0'  # 8 GPU 를 사용할 것 인지 정하는 옵션 ( 0 or 1 )  args[6]     # gpu 를 사용하면 cuda 는 1개만 사용, memory 사용량 확인. # cpu를 사용하면 자동으로 직렬

cuda_dict = {'cuda0': 20}  # 각 cuda 사용 가능한 memory 입력, cuda 가 늘어날 경우 맞춰서 입력
ram_base_memory = 5  # 기본적으로 사용하고 있는 memory
ram_total_memory = 30  # 총 memory

use_gpu_memory = 2  # predict 할때 사용 하는 gpu 메모리
use_ram_memory = 2  # predict 할때 사용 하는 gpu 메모리

mha_root = r'D:/538ons_vol_temp/export_volume_template/input'  # 추론 할 image 폴더가 모여 있는 폴더 경로
batch_loc = r'C:\Users\3DONS\Desktop\temp_preshin'  # batch 파일을 생성할 폴더 경로

batch_folder_name = 'predict_batch'  # 배치 파일이 들어갈 폴더 이름
batch_file_name = 'temp'  # 배치 파일 명

##############################################################################

total_cup_memory_bat = (ram_total_memory - ram_base_memory) // use_ram_memory
total_gpu_memory_bat = cuda_dict['cuda0'] / use_gpu_memory
bat_memory = [total_gpu_memory_bat, total_cup_memory_bat]


#  mha 파일과 id 폴더를 dict 로 만듬
def return_mha_dir_filename(root_loc: str):
    mha_folder_id = {}
    mha_folder_list = os.listdir(root_loc)  # predict 할 id 폴더 list

    for i in mha_folder_list:
        mha_file = ''
        mha_file_list = os.listdir(f'{root_loc}/{i}')  # predict 할 id 폴더 안의 파일 list
        for j in mha_file_list:
            if 'mha' in j:  # mha 파일만 추가
                mha_file = j
                break

        mha_folder_id[i] = mha_file

    return mha_folder_id


# 배치 파일 생성
def make_cpu_batch(id_mha_dict: dict, root_loc: str, bat_loc: str, memory: list, *args):

    total_predict = len(id_mha_dict)    # 총 predict 개수

    list_keys = list(id_mha_dict.keys())  # key : id

    os.mkdir(f'{bat_loc}/{batch_folder_name}')  # batch 파일 넣을 폴더 생성

    pre_in_batch = []
    count = 0  # count 로 나머지 계산

    if args[6] != '0':

        print('GPU 사용')
        print(f'----사용 가능 GPU Batch 개수 : {int(memory[0])}')
        print(f'----사용 가능 CPU Batch 개수 : {int(memory[1])}')
        # print(f'    총 predict 개수 : {total_predict}')
        memory.sort()  # sort 해서 적은수 앞으로 놓고 앞에 기준으로 bat 파일 개수 지정
        pre_num = int(total_predict//round((memory[0]), 0))
        bat_num = int(round((memory[0]), 0))
        print(f'----Batch 개수가 작은 것 사용\n')

    else:
        print('CPU 사용')
        pre_num = len(id_mha_dict)
        bat_num = 1
    rest_predict = total_predict % pre_num  # 남은 predict 개수
    insert_predict = rest_predict // bat_num  # batch 하나당 추가 하는 predict 개수
    insert_rest_predict = rest_predict % bat_num  # batch 에 한개씩 추가 하는 나머지 predict 개수

    print(f'    총 predict 개수 : {total_predict}')
    print(f'    총 batch 개수 : {bat_num}')
    print(f'    batch 한 개당 predict 개수 : {pre_num} 남은 개수 : {rest_predict}')
    print(f'    남은 개수 분배 : batch 에 {insert_predict}개 씩 추가, 남은 {insert_rest_predict}개 앞에 하나씩 추가')

    for i in range(total_predict // pre_num):  # 총 배치 파일 개수

        # with open(f'{bat_loc}/{batch_folder_name}/{batch_file_name}{i}.bat', 'a') as f:
        #     f.write(f'')      # 추가

        if insert_rest_predict > 0:  # 차감 하는 방식 으로 나머지를 하나씩 추가 후 차감해 0 이되면 추가 하지 않도록 함
            rest = 1
        else:
            rest = 0

        pre_in_batch.append(pre_num + insert_predict + rest)  # 지워도 됨, 단순히 batch 파일 하나 당 predict 개수 확인용

        for j in range(pre_num + insert_predict + rest):  # predict 개수
            with open(f'{bat_loc}/{batch_folder_name}/{batch_file_name}{i}.bat', 'a') as f:
                f.write(f'{args[0]} {args[1]} {args[2]} {args[3]} {root_loc}/{list_keys[count]} {id_mha_dict[list_keys[count]]} {args[4]} {args[5]} {args[6]}\n')
            count += 1  # count 로 index 기억

        insert_rest_predict -= 1  # 나머지 개수 차감

    print(f'    생성 되는 predict 개수 {pre_in_batch}')


# 배치 파일 한번에 실행하는 배치 파일 제작
def total_start_batch(bat_loc: str):
    file_list = os.listdir(f'{bat_loc}/{batch_folder_name}')
    with open(f'{bat_loc}/{batch_folder_name}/start_total_batch.bat', 'a') as f:
        for j in file_list:
            f.write(f'start "{j}" "{bat_loc}/{batch_folder_name}/{j}"\n')  # 띄어쓰기, 스페이스바 확인. 하나 차이로 오류발생


mha_dict = return_mha_dir_filename(mha_root)
make_cpu_batch(mha_dict, mha_root, batch_loc, bat_memory, file_name, key, result_report_path, root_dir, model_dir, output_path, use_gpu)
total_start_batch(batch_loc)
