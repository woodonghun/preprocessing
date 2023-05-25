import os

import SimpleITK as sitk

"""
    nrrd와 mhd 의 사이즈가 다른 경우 발생하여 검증하는 코드 제작
    image 파일과 mhd 파일은 같은 경로 => 다를시 주소만 수정
"""

inputDir = r'\\192.168.0.42\share\temp\tooth_size_mis\mis'


def Verification(dir: str):

    all_data = os.listdir(dir)
    name_list = []
    for i in all_data:
        if '_lnd' not in i:
            name_list.append(i.split('.')[0])

    file_name_list = list(set(name_list))

    for j in file_name_list:
        # mhd 이미지 로딩
        reader = sitk.ImageFileReader()
        reader.SetImageIO('MetaImageIO')
        reader.SetFileName(inputDir + '/' + j + '.mhd')
        imgOrg: sitk.Image = reader.Execute()


        reader.SetImageIO('NrrdImageIO')
        reader.SetFileName(inputDir + '/' + j + '.nrrd')
        imgLabel: sitk.Image = reader.Execute()

        print(j,imgOrg.GetSize(), imgLabel.GetSize())
        if imgOrg.GetSize() != imgLabel.GetSize():
            print(j)

if __name__ == '__main__':
    Verification(inputDir)