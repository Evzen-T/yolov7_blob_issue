# Yolov7 blob inferencing issue

## How to reproduce?
1. Download coco dataset from yolov7
    - git clone https://github.com/WongKinYiu/yolov7.git
    - pip install -r requirements.txt
    - pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116
    - bash scripts/get_coco.sh

2. Train coco dataset with yolov7-tiny weights
    - cd ./yolov7
    - python3 train.py --img 640 640 --epochs 100 --batch-size 32 --data data/coco.yaml --cfg ./cfg/training/yolov7-tiny.yaml --weights yolov7-tiny.pt --device 0 --workers 8

3. Convert to blob file
    - Using > https://tools.luxonis.com/
    - Insert trained coco yolov7-tiny
    - Insert 640 as image size

4. Run inference
    - cd yolov7_blob_issue

    **Pytorch**
    - Insert local location of yolov7 pt weights into pt_oak.py
    - Insert location of trained coco yolov7-tiny pt weights into pt_oak.py
    - python3 pt_oak.py

    **Blob**
    - Insert location of trained coco yolov7-tiny blob weights into blob_oak.py
    - Insert location of trained coco yolov7-tiny json config into blob_oak.py
    - python3 blob_oak.py