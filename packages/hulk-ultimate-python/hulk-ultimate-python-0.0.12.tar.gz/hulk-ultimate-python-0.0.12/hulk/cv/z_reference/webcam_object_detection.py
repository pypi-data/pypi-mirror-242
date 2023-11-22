import cv2 #line:1
from hulk import YOLOv8 #line:3
cap =cv2 .VideoCapture (0 )#line:6
model_path ="../models/宜昌-点位1.onnx"#line:8
yolov8_detector =YOLOv8 (model_path ,iConfThreshold =0.5 ,iIouThreshold =0.5 )#line:9
cv2 .namedWindow ("Detected Objects",cv2 .WINDOW_NORMAL )#line:11
while cap .isOpened ():#line:12
    ret ,frame =cap .read ()#line:14
    if not ret :#line:16
        break #line:17
    boxes ,scores ,class_ids =yolov8_detector (frame )#line:20
    combined_img =yolov8_detector .drawDetections (frame )#line:22
    cv2 .imshow ("Detected Objects",combined_img )#line:23
    if cv2 .waitKey (1 )&0xFF ==ord ('q'):#line:26
        break #line:27
