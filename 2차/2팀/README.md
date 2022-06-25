# Project Description (211018 ~ 211112, 약 4주간 진행)
* 전반적인 설명은 ppt_and_images에 있는 PPT를 참고해주세요. 

## 프로젝트 주제
<div align="center">
<img src="https://github.com/0Oong/cakd3_2nd_project-mold_detection/blob/main/ppt_and_images/%E1%84%8C%E1%85%AE%E1%84%8C%E1%85%A6.png" width="60%"> 
  
설명 : 약용작물 중 하나인 밀순의 흰 곰팡이를 탐지하는 프로그램
</div>



## 팀원 소개
<div align="center">
<img src="https://github.com/0Oong/cakd3_2nd_project-mold_detection/blob/main/ppt_and_images/%E1%84%90%E1%85%B5%E1%86%B7%E1%84%8B%E1%85%AF%E1%86%AB.png" width="60%">
</div>

## 프로젝트 목차 
<div align="center">
<img src="https://github.com/0Oong/cakd3_2nd_project-mold_detection/blob/main/ppt_and_images/%E1%84%86%E1%85%A9%E1%86%A8%E1%84%8E%E1%85%A1.png" width="60%">
</div>

# HOW TO RUN
#### 0. 모든 파일들을 다운받아 yolov5라는 폴더를 만들어 넣는다. 
best.pt파일은 압축을 풀어 넣는다. 



### 1. Anaconda(www.anaconda.com) Individual Edition을 다운로드해 설치한다.
테스트에 사용한 버전은 2021.05버전이다.



### 2. 아나콘다 프롬프트를 실행시키고 필요한 라이브러를 설치한다.
```
pip install -r requirements.txt
```



### 3. 파이썬으로 detect.py를 실행시킨다. 
yolov5/images 디렉토리에 탐지할 원본이미를 넣고 다음과 같이 실행시키면 현재 폴더에 result 디렉토리가 생성되고 그 안에 곰팡이가 탐지된 이미지가 생성된다.
```
python yolov5/detect.py --source ./yolov5/images --project ./
```

# Datasets annotation
### DATASETS
https://public.roboflow.ai/object-detection/undefined

### This dataset was exported via roboflow.ai

It includes 385 images.
Mold are annotated in YOLO v5 PyTorch format.

The following pre-processing was applied to each image:
* Auto-orientation of pixel data (with EXIF-orientation stripping)
* Resize to 600x416 (Stretch)

The following augmentation was applied to create 3 versions of each source image:
* 50% probability of horizontal flip
* Randomly crop between 0 and 20 percent of the image
* Random exposure adjustment of between -25 and +25 percent

# 사용 모델 및 라이브러리
* YOLO v5 : 주 사용모델
(https://github.com/ultralytics/yolov5)
* ROBOFLOW : annotation tool
(https://roboflow.com/)
* Pytorch
* OpenCV
