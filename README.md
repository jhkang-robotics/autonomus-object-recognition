# autonomus-object-recognition
자율주행영상 객체검출경진대회

0. GPU: RTX 2080Ti *2 / cudatoolkit: 11.3.1 / cudnn: 8.2.1.32
1. Todo: pip install -r requirements.txt

2. 본 코드는 YOLO 타입의 Annotations 타입을 지원하기에 주최측에서 제공된 Annotations 타입인 xml 파일을 yolo 타입으로 변환 필요.

# 작업 간편화를 위해 학습데이터를 /VOCdevkit/VOC2007/JPEGImages 폴더 최상단으로 이동
# Annotations xml 파일 역시 /VOCdevkit/VOC2007/Annotations 폴더 최상단으로 이동
# 모든 파일명을 /VOCdevkit/VOC2007/ImageSets/Main/train.txt 파일에 작성
# data_type_trans 폴더의 voc_label.py 파일 실행시 /VOCdevkit/VOC2007/labels 폴더에 변환된 xml 파일 생성



# train을 위해 data/coco.yaml 파일에서 학습데이터 경로 설정 및 클래스 갯수 및 이름 지정 
3. Train: 

python -m torch.distributed.run --nproc_per_node 2 train.py --batch 2 --data coco.yaml  --weights weights/yolov5l6.pt --cfg yolov5l.yaml --img 1280 --device 0,1


# train을 하면 runs/train/exp/weights 폴더에 best.pt, last.pt 가중치 파일 생성
# best.pt 파일을 weights/ 폴더에 복사
# --source * 에 추론하고자 하는 데이터 폴더 경로 지정
# weight 파일의 용량이 큰 문제로 인해 github에 업로드 불가. 때문에 https://drive.google.com/file/d/1QeC7VOMYUoV3m6f4sUzaa-Qd4S1_cjtg/view?usp=sharing 다음 링크에서 학습된 weight 파일 다운 후 재헌 가능 

4. Infrance: 

python detect.py --source data/test/ --weights weights/best.pt --save-txt --save-crop --device 0,1 --img-size 1280


# Infrance과정이 진행되면 /runs/detect/exp/lavels 폴더가 생성되면서 해당 폴더안에 Infrance 결과 Annotations 파일 생성
# yolo 타입의 Annotations 파일을 xml 타입으로 변환하기 위해 data_type_trans 폴더의 txt_to_xml.py 파일 실행하면 설정된 save_path의 폴더에 .xml 타입의 Annotations 파일 생성     
