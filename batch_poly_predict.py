import os

parm0 = 'ON3D_Tooth_Seg_Poly.exe'  # AI 프로그램 실행파일
parm1 = '94jkl4#56*f#'  # 프로그램 구동용 비밀키
# parm2 = 'input_dir'  # input_dir   아래의 input_dir_root 와 split_input_list 를 조합 해서 사용함
parm3 = r'C:\Users\3DONS\Desktop\temp\output'  # output_dir
# parm4 = 'ON3D_Random_ID'  # ON3D_Random_Id 이지만 결과 확인용으론 input 넣으면됨
parm5 = 'LL1,LL2,LL3,LL4,LL5,LL6,LL7,LL8,' \
        'LU1,LU2,LU3,LU4,LU5,LU6,LU7,LU8,' \
        'RL1,RL2,RL3,RL4,RL5,RL6,RL7,RL8,' \
        'RU1,RU2,RU3,RU4,RU5,RU6,RU7,RU8'
parm6 = 0  # threshold default 0

batch_folder_name = 'poly_pre_batch'

drive_loc = 'C:'
bat_loc = r'C:\Users\3DONS\Desktop\temp\batch'  # bat 를 생성할 위치
exe_dir = r'C:\Users\3DONS\Desktop\train_predict_code\Crown_Poly_Seg_exe\total_import'  # predict exe 파일의 위치
# env_name = ''  # 가상 환경 이름 exe 는 가상환경 필요없음
input_dir_root = r'C:\Users\3DONS\Desktop\Augmentation Code\AI Polygon Segmentation\Dentition_Crop\data\output_dir\WDI'  # input 해야 하는 폴더가 모여 있는 루트
bat_size = 3  # 생성할 batch 파일의 개수


def split_input_list(input_root):
    input_list = os.listdir(input_root)

    # 폴더만 포함하도록 필터링
    input_list = [item for item in input_list if os.path.isdir(os.path.join(input_root, item))]

    part_size = len(input_list) // bat_size
    remainder = len(input_list) % bat_size  # 나머지 항목 계산

    input_parts = {}

    start_index = 0

    for i in range(bat_size):
        end_index = start_index + part_size

        # 나머지 항목을 중간에 추가
        if remainder > 0:
            end_index += 1
            remainder -= 1

        part_name = f"part{i + 1}"
        input_parts[part_name] = input_list[start_index:end_index]
        start_index = end_index

    # 결과 출력
    for part_name, part_data in input_parts.items():
        print(f"{part_name}: {part_data}")

    return input_parts


def make_bat(p0, p1, input_root, p3, p5, p6, batch_location):
    input_dict = split_input_list(input_root)
    for part_name, part_data in input_dict.items():
        for i in part_data:
            with open(f'{batch_location}/{part_name}.bat', 'a') as f:
                f.write(f'{p0} {p1} {input_root}\{i} {p3} {i} {p5} {p6}\n')


def total_start_batch(batch_location: str):
    file_list = os.listdir(fr'{batch_location}')
    with open(fr'{batch_location}\start_total_batch.bat', 'a') as f:
        f.write(f"{drive_loc}\n")
        f.write(f"cd {exe_dir}\n")
        # f.write(f'call conda activate {env_name}\n')
        for j in file_list:
            if 'bat' in j:
                f.write(f'start "{j}" "{batch_location}\{j}"\n')  # 띄어쓰기, 스페이스바 확인. 하나 차이로 오류발생


if __name__ == "__main__":
    make_bat(parm0, parm1, input_dir_root, parm3, parm5, parm6, bat_loc)
    total_start_batch(bat_loc)
