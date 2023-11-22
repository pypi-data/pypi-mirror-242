import cv2 #line:1
from hulk import YOLOv8 #line:3
cap =cv2 .VideoCapture ("http://localhost:8000/2.mp4")#line:6
model_path ="../models/宜昌-点位1.onnx"#line:12
yolov8_detector =YOLOv8 (model_path ,iConfThreshold =0.5 ,iIouThreshold =0.5 )#line:13
cv2 .namedWindow ("Detected Objects",cv2 .WINDOW_NORMAL )#line:15
while cap .isOpened ():#line:16
    if cv2 .waitKey (1 )==ord ('q'):#line:18
        break #line:19
    try :#line:21
        ret ,frame =cap .read ()#line:23
        if not ret :#line:24
            break #line:25
    except Exception as e :#line:26
        print (e )#line:27
        continue #line:28
    boxes ,scores ,class_ids =yolov8_detector (frame )#line:31
    combined_img =yolov8_detector .drawDetections (frame )#line:33
    cv2 .imshow ("Detected Objects",combined_img )#line:34
