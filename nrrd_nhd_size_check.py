import os
from tqdm import tqdm
import SimpleITK as sitk

"""
    nrrd와 mhd 의 사이즈가 다른 경우 발생하여 검증하는 코드 제작
    폴더명이 한글이면 동작하지 않음
    출력이 끝나면 finish print
"""

input_nrrd = r'D:\Segmentation_project\Segmentation merge\mx_mn_tooth_merge\mn_merge\train'
input_image = r'D:\Segmentation_project\AI Segmentation Label Folder\AI Mn, Mx Segmentation\train\Image'
label_folder_name = r'test'


def Verification(image_dir: str, nrrd_dir: str):
    print('size 다른 파일 목록 출력')
    all_data = os.listdir(image_dir)  # image 파일의 경로
    name_list = []
    error_list = []

    for i in all_data:
        if '_lnd' not in i:
            name_list.append(i.split('.')[0])
    file_name_list = sorted(list(set(name_list)))

    for j in tqdm(file_name_list):
        # mhd 이미지 로딩
        reader = sitk.ImageFileReader()
        reader.SetImageIO('MetaImageIO')
        reader.SetFileName(image_dir + '/' + j + '.mhd')  # 파일들이 하나의 경로에 존재할때
        # reader.SetFileName(inputDir + '/image/' + j.replace('#mx', '') + '.mhd')
        # reader.SetFileName(inputDir + '/image/' + j.replace('#mx', '').replace('#mn', '') + '.mhd')
        imgOrg: sitk.Image = reader.Execute()

        # nrrd 로딩
        reader.SetImageIO('NrrdImageIO')
        # reader.SetFileName(inputDir + '/' + j + '.nrrd')
        reader.SetFileName(nrrd_dir + '/' + j + '.nrrd')
        try:
            imgLabel: sitk.Image = reader.Execute()
        except:
            continue
        if imgOrg.GetSize() != imgLabel.GetSize():  # size 다를 경우에 출력
            print(f' image_id : {j}   \tmhd_size : {imgOrg.GetSize()}    \tnrrd_size : {imgLabel.GetSize()}')
            error_list.append(j)

    print(f'총 개수 : {len(error_list)}')
    print(f'image name list : {error_list}')


if __name__ == '__main__':
    Verification(input_image, input_nrrd)
