import os

'''
    ON3DS landmark 추론 batch 파일 생성 코드
'''

drive_loc = 'C:'
python_path = r'C:\Users\3DONS\Desktop\train_predict_code\ON3DS_3D_predict_code'

file_name = r'ON3DS_PreShinS3D.py'  # 0 AI 프로그램 실행 파일   args[0]
key = '94jkl4#56*f#'  # 1 프로그램 구동용 비밀키 아무거나 넣어도됨  args[1]
result_report_path = r'C:\Users\3DONS\Desktop\train_predict_code\ON3DS_3D_predict_code\ON3DS_PreShinS3D_result_report.dat'  # 2 결과 리포트 파일의 경로  args[2]
root_dir = r'C:\Users\3DONS\Desktop\train_predict_code\ON3DS_3D_predict_code'  # 3 "/ON3DS/AI 폴더의 절대 경로"    args[3]
# mhd_dir = 'temp6'  # 4 추론 할 image 파일이 있는 폴더 경로                4,5 번 은 코드 내에서 추가
# mhd_filename = 'temp7'  # 5 추론 한 예측 결과를 저장할 경로
model_dir = r'C:\Users\3DONS\Desktop\train_predict_code\ON3DS_3D_predict_code\ON3DS_PreShinS3D_F\weight'  # 6 pth 파일이 있는 폴더 경로 args[4]
output_path = r'C:\20230703_ON3DS\predict'  # 7 추론 한 예측결과를 저장할 경로 args[5]
points = '17,18,19,15,16,30,31,21,20,23,22,144,145,34,24,25,26,27,28,29,32,33,142,143,36,37,65,66,52,53,91,92,38,39,67,68,54,55,93,94,70,71,40,41,95,96,56,57,73,74,76,' \
         '77,97,98,99,100,43,44,78,79,58,59,101,102,45,46,80,81,60,61,103,104,83,84,47,48,105,106,62,63,86,87,89,90,107,108,109,110,69,72,42,75,82,85,49,88,140,141,' \
         '120,123,124,121,122,125,126,129,35,51,127,128,131,132,139,130,137,138,134,133,135,136'  # 8 추론할 랜드마크  args[6]
overwrite_cache = 'True'  # 9 caching 파일을 덮어쓰기 하는 옵션(무조건 True)  args[7]
use_gpu = 'False'  # 10 GPU 를 사용할 것 인지 정하는 옵션 (무조건 False)  args[8]
cuda_id = '0'  # 11 멀티 cuda GPU 사용을 가정하고 GPU선택 (무조건 0)  args[9]
use_gold_resize = 'False'  # 12 분석이 끝나지 않는 인자 (무조건 False)  args[10]
test = 'False'  # 13 test 모드를 쓸것인가 선택하는 모드 (무조건 False)  args[11]

# gpu 만 사용하면 cpu 수정 안해도 무관
cuda_dict = {'cuda0': 4}  # 각 cuda 사용 가능한 memory 입력, cuda 가 늘어날 경우 맞춰서 입력
cpu_base_memory = 7  # 기본적으로 사용하고 있는 memory
cpu_total_memory = 14  # 총 memory

use_gpu_memory = 2  # predict 할때 사용 하는 gpu 메모리
use_cpu_memory = 2  # predict 할때 사용 하는 cpu 메모리

mhd_root = r"C:\20230703_ON3DS\image"  # 추론 할 image 폴더가 모여 있는 폴더 경로
batch_loc = r'C:\20230703_ON3DS'  # batch 파일을 생성할 폴더 경로

batch_folder_name = 'valid_train'  # 배치 파일이 들어갈 폴더 이름
batch_file_name = 'temp'  # 배치 파일 명

##############################################################################

total_cup_memory_bat = (cpu_total_memory - cpu_base_memory) // use_cpu_memory
total_gpu_memory_bat = cuda_dict['cuda0'] / use_gpu_memory
bat_memory = [total_gpu_memory_bat, total_cup_memory_bat]


#  mha 파일과 id 폴더를 dict 로 만듬
def return_mhd_dir_filename(root_loc: str):
    mhd_folder_id = {}
    mhd_folder_list = os.listdir(root_loc)  # predict 할 id 폴더 list

    for i in mhd_folder_list:
        print(i)
        if 'mhd' in i:  # mha 파일만 추가
            patient = i.split('.')[0]
            mhd_folder_id[patient] = i

    print(mhd_folder_id)
    return mhd_folder_id


# 배치 파일 생성
def make_cpu_batch(id_mha_dict: dict, root_loc: str, bat_loc: str, memory: list, *args):

    total_predict = len(id_mha_dict)    # 총 predict 개수

    list_keys = list(id_mha_dict.keys())  # key : id

    os.mkdir(f'{bat_loc}/{batch_folder_name}')  # batch 파일 넣을 폴더 생성

    pre_in_batch = []
    count = 0  # count 로 나머지 계산

    if args[8] != 'False':

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
        pre_num = int(total_predict // round((memory[1]), 0))
        bat_num = int(round((memory[1]), 0))
    rest_predict = total_predict % pre_num  # 남은 predict 개수
    insert_predict = rest_predict // bat_num  # batch 하나당 추가 하는 predict 개수
    insert_rest_predict = rest_predict % bat_num  # batch 에 한개씩 추가 하는 나머지 predict 개수

    print(f'    총 predict 개수 : {total_predict}')
    print(f'    총 batch 개수 : {bat_num}')
    print(f'    batch 한 개당 predict 개수 : {pre_num} 남은 개수 : {rest_predict}')
    print(f'    남은 개수 분배 : batch 에 {insert_predict}개 씩 추가, 남은 {insert_rest_predict}개 앞에 하나씩 추가')



    for i in range(total_predict // pre_num):  # 총 배치 파일 개수
        with open(f'{bat_loc}/{batch_folder_name}/{batch_file_name}{i}.bat', 'a') as f:
            f.write(f'{drive_loc}\n')
            f.write(f"cd {python_path}\n")
            f.write(f"call conda activate tempallpk\n")
        # with open(f'{bat_loc}/{batch_folder_name}/{batch_file_name}{i}.bat', 'a') as f:
        #     f.write(f'')      # 추가

        if insert_rest_predict > 0:  # 차감 하는 방식 으로 나머지를 하나씩 추가 후 차감해 0 이되면 추가 하지 않도록 함
            rest = 1
        else:
            rest = 0

        pre_in_batch.append(pre_num + insert_predict + rest)  # 지워도 됨, 단순히 batch 파일 하나 당 predict 개수 확인용

        for j in range(pre_num + insert_predict + rest):  # predict 개수
            with open(f'{bat_loc}/{batch_folder_name}/{batch_file_name}{i}.bat', 'a') as f:
                f.write(f'python {args[0]} {args[1]} {args[2]} {args[3]} {root_loc} {id_mha_dict[list_keys[count]]} {args[4]} {args[5]}\{id_mha_dict[list_keys[count]].split(".")[0]}.dat {str(args[6])} {args[7]}'
                        f' {args[8]} {args[9]} {args[10]} {args[11]}\n')
            count += 1  # count 로 index 기억

        insert_rest_predict -= 1  # 나머지 개수 차감

    print(f'    생성 되는 predict 개수 {pre_in_batch}')


# 배치 파일 한번에 실행하는 배치 파일 제작
def total_start_batch(bat_loc: str):
    file_list = os.listdir(f'{bat_loc}/{batch_folder_name}')
    with open(f'{bat_loc}/{batch_folder_name}/start_total_batch.bat', 'a') as f:
        f.write(f"{drive_loc}\n")
        f.write(f"cd {python_path}\n")
        f.write('call conda activate tempallpk\n')
        for j in file_list:
            f.write(f'start "{j}" "{bat_loc}/{batch_folder_name}/{j}"\n')  # 띄어쓰기, 스페이스바 확인. 하나 차이로 오류발생
        f.write('pause\n')


mhd_dict = return_mhd_dir_filename(mhd_root)
make_cpu_batch(mhd_dict, mhd_root, batch_loc, bat_memory, file_name, key, result_report_path, root_dir, model_dir, output_path, points, overwrite_cache, use_gpu, cuda_id, use_gold_resize, test)
total_start_batch(batch_loc)
