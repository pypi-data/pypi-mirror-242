import cv2 #line:1
from imread_from_url import imread_from_url #line:2
from PIL import Image #line:3
import numpy as np #line:4
from hulk import YOLOv8 #line:6
model_path ="../models/宜昌-点位1.onnx"#line:8
yolov8_detector =YOLOv8 (model_path ,iConfThreshold =0.2 ,iIouThreshold =0.3 )#line:9
img_url ="http://localhost:8000/1.jpg"#line:12
img =imread_from_url (img_url )#line:13
img =Image .open ('../test/1.jpg').convert ('RGB')#line:15
img =np .array (img )#line:16
img =img [:,:,::-1 ].copy ()#line:17
img =cv2 .cvtColor (np .array (img ,dtype =np .uint8 ),cv2 .COLOR_RGB2BGR )#line:18
boxes ,scores ,class_ids =yolov8_detector (img )#line:21
combined_img =yolov8_detector .drawDetections (img )#line:24
cv2 .namedWindow ("Detected Objects",cv2 .WINDOW_NORMAL )#line:25
cv2 .imshow ("Detected Objects",combined_img )#line:26
cv2 .imwrite ("doc/img/1.jpg",combined_img )#line:27
cv2 .waitKey (0 )#line:28
