import time #line:1
import cv2 #line:2
import numpy as np #line:3
import onnxruntime #line:4
class_names =['person','bicycle','car','motorcycle','airplane','bus','train','truck','boat','traffic light','fire hydrant','stop sign','parking meter','bench','bird','cat','dog','horse','sheep','cow','elephant','bear','zebra','giraffe','backpack','umbrella','handbag','tie','suitcase','frisbee','skis','snowboard','sports ball','kite','baseball bat','baseball glove','skateboard','surfboard','tennis racket','bottle','wine glass','cup','fork','knife','spoon','bowl','banana','apple','sandwich','orange','broccoli','carrot','hot dog','pizza','donut','cake','chair','couch','potted plant','bed','dining table','toilet','tv','laptop','mouse','remote','keyboard','cell phone','microwave','oven','toaster','sink','refrigerator','book','clock','vase','scissors','teddy bear','hair drier','toothbrush']#line:14
rng =np .random .default_rng (3 )#line:17
colors =rng .uniform (0 ,255 ,size =(len (class_names ),3 ))#line:18
class YoloUtils :#line:21
    @staticmethod #line:22
    def nms (O0OOOO0OO0O00O0O0 ,O0O0000O0OO0O0O0O ,OO000O0000OO00OO0 ):#line:23
        O0O0OO0O0OO0O0O0O =np .argsort (O0O0000O0OO0O0O0O )[::-1 ]#line:25
        OOO0000O0OO0O0000 =[]#line:27
        while O0O0OO0O0OO0O0O0O .size >0 :#line:28
            O0O0O0OOOOOO00O0O =O0O0OO0O0OO0O0O0O [0 ]#line:30
            OOO0000O0OO0O0000 .append (O0O0O0OOOOOO00O0O )#line:31
            OO0000O0O00OOOO0O =YoloUtils .compute_iou (O0OOOO0OO0O00O0O0 [O0O0O0OOOOOO00O0O ,:],O0OOOO0OO0O00O0O0 [O0O0OO0O0OO0O0O0O [1 :],:])#line:34
            OO000O000O0OO00OO =np .where (OO0000O0O00OOOO0O <OO000O0000OO00OO0 )[0 ]#line:37
            O0O0OO0O0OO0O0O0O =O0O0OO0O0OO0O0O0O [OO000O000O0OO00OO +1 ]#line:40
        return OOO0000O0OO0O0000 #line:42
    @staticmethod #line:44
    def compute_iou (O000O0OO00OO0OO00 ,OOOO00OOO0OOO000O ):#line:46
        OOOOOO00O0O0OO0O0 =np .maximum (O000O0OO00OO0OO00 [0 ],OOOO00OOO0OOO000O [:,0 ])#line:48
        O00OOO00OOO000000 =np .maximum (O000O0OO00OO0OO00 [1 ],OOOO00OOO0OOO000O [:,1 ])#line:49
        OOO000OO00OOO00O0 =np .minimum (O000O0OO00OO0OO00 [2 ],OOOO00OOO0OOO000O [:,2 ])#line:50
        O00OO0O0OO0OOO00O =np .minimum (O000O0OO00OO0OO00 [3 ],OOOO00OOO0OOO000O [:,3 ])#line:51
        OO0O0O0OOO000O0OO =np .maximum (0 ,OOO000OO00OOO00O0 -OOOOOO00O0O0OO0O0 )*np .maximum (0 ,O00OO0O0OO0OOO00O -O00OOO00OOO000000 )#line:54
        O0000OOOOO0O0O000 =(O000O0OO00OO0OO00 [2 ]-O000O0OO00OO0OO00 [0 ])*(O000O0OO00OO0OO00 [3 ]-O000O0OO00OO0OO00 [1 ])#line:57
        O00000OOO0OOOOOO0 =(OOOO00OOO0OOO000O [:,2 ]-OOOO00OOO0OOO000O [:,0 ])*(OOOO00OOO0OOO000O [:,3 ]-OOOO00OOO0OOO000O [:,1 ])#line:58
        OOOO00O0000OO0O00 =O0000OOOOO0O0O000 +O00000OOO0OOOOOO0 -OO0O0O0OOO000O0OO #line:59
        O00O0OOOO00OO0O0O =OO0O0O0OOO000O0OO /OOOO00O0000OO0O00 #line:62
        return O00O0OOOO00OO0O0O #line:64
    @staticmethod #line:66
    def xywh2xyxy (OOO0O0OO0O000OOOO ):#line:68
        O0O0O00OOO000OOO0 =np .copy (OOO0O0OO0O000OOOO )#line:70
        O0O0O00OOO000OOO0 [...,0 ]=OOO0O0OO0O000OOOO [...,0 ]-OOO0O0OO0O000OOOO [...,2 ]/2 #line:71
        O0O0O00OOO000OOO0 [...,1 ]=OOO0O0OO0O000OOOO [...,1 ]-OOO0O0OO0O000OOOO [...,3 ]/2 #line:72
        O0O0O00OOO000OOO0 [...,2 ]=OOO0O0OO0O000OOOO [...,0 ]+OOO0O0OO0O000OOOO [...,2 ]/2 #line:73
        O0O0O00OOO000OOO0 [...,3 ]=OOO0O0OO0O000OOOO [...,1 ]+OOO0O0OO0O000OOOO [...,3 ]/2 #line:74
        return O0O0O00OOO000OOO0 #line:75
    @staticmethod #line:77
    def drawDetections (O0000OO0OOO0O0O00 ,OOO000O0OOOO0000O ,O0000OOOOOOOOO00O ,OOO0000O0O0O00000 ,mask_alpha =0.3 ):#line:78
        OO0O0O00O000O000O =O0000OO0OOO0O0O00 .copy ()#line:79
        O00OO0OOO0000OO0O =O0000OO0OOO0O0O00 .copy ()#line:80
        OO0OO000O000O0OO0 ,O00OO0OOO0O000O00 =O0000OO0OOO0O0O00 .shape [:2 ]#line:82
        O0OO0000O00O00OO0 =min ([OO0OO000O000O0OO0 ,O00OO0OOO0O000O00 ])*0.0006 #line:83
        O00O0O00O000000OO =int (min ([OO0OO000O000O0OO0 ,O00OO0OOO0O000O00 ])*0.001 )#line:84
        for O00O00OOOOOO0O000 ,OO0OOO00OO0O000OO ,OOO0O000OO0000O0O in zip (OOO000O0OOOO0000O ,O0000OOOOOOOOO00O ,OOO0000O0O0O00000 ):#line:87
            O0OO0OOO0OOOO0OO0 =colors [OOO0O000OO0000O0O ]#line:88
            O0000O0O00O00OOOO ,O0O0O0O0O00OO0OOO ,OOO00OO000OOO0OOO ,O00O0O000O0O0OOOO =O00O00OOOOOO0O000 .astype (int )#line:90
            cv2 .rectangle (O00OO0OOO0000OO0O ,(O0000O0O00O00OOOO ,O0O0O0O0O00OO0OOO ),(OOO00OO000OOO0OOO ,O00O0O000O0O0OOOO ),O0OO0OOO0OOOO0OO0 ,2 )#line:93
            cv2 .rectangle (OO0O0O00O000O000O ,(O0000O0O00O00OOOO ,O0O0O0O0O00OO0OOO ),(OOO00OO000OOO0OOO ,O00O0O000O0O0OOOO ),O0OO0OOO0OOOO0OO0 ,-1 )#line:96
            O00OOO00O000O0O0O =class_names [OOO0O000OO0000O0O ]#line:98
            OOOOO000O0OOO0O00 =f'{O00OOO00O000O0O0O} {int(OO0OOO00OO0O000OO * 100)}%'#line:99
            (OOO00O0O0OOOO0000 ,OO0OOOO0OO00O0O00 ),_O00O0O00OOO0OO0O0 =cv2 .getTextSize (text =OOOOO000O0OOO0O00 ,fontFace =cv2 .FONT_HERSHEY_SIMPLEX ,fontScale =O0OO0000O00O00OO0 ,thickness =O00O0O00O000000OO )#line:101
            OO0OOOO0OO00O0O00 =int (OO0OOOO0OO00O0O00 *1.2 )#line:102
            cv2 .rectangle (O00OO0OOO0000OO0O ,(O0000O0O00O00OOOO ,O0O0O0O0O00OO0OOO ),(O0000O0O00O00OOOO +OOO00O0O0OOOO0000 ,O0O0O0O0O00OO0OOO -OO0OOOO0OO00O0O00 ),O0OO0OOO0OOOO0OO0 ,-1 )#line:105
            cv2 .rectangle (OO0O0O00O000O000O ,(O0000O0O00O00OOOO ,O0O0O0O0O00OO0OOO ),(O0000O0O00O00OOOO +OOO00O0O0OOOO0000 ,O0O0O0O0O00OO0OOO -OO0OOOO0OO00O0O00 ),O0OO0OOO0OOOO0OO0 ,-1 )#line:107
            cv2 .putText (O00OO0OOO0000OO0O ,OOOOO000O0OOO0O00 ,(O0000O0O00O00OOOO ,O0O0O0O0O00OO0OOO ),cv2 .FONT_HERSHEY_SIMPLEX ,O0OO0000O00O00OO0 ,(255 ,255 ,255 ),O00O0O00O000000OO ,cv2 .LINE_AA )#line:109
            cv2 .putText (OO0O0O00O000O000O ,OOOOO000O0OOO0O00 ,(O0000O0O00O00OOOO ,O0O0O0O0O00OO0OOO ),cv2 .FONT_HERSHEY_SIMPLEX ,O0OO0000O00O00OO0 ,(255 ,255 ,255 ),O00O0O00O000000OO ,cv2 .LINE_AA )#line:112
        return cv2 .addWeighted (OO0O0O00O000O000O ,mask_alpha ,O00OO0OOO0000OO0O ,1 -mask_alpha ,0 )#line:114
    @staticmethod #line:116
    def draw_comparison (O0000O0O0O0OOOOO0 ,O00O0O00O0000O000 ,OOO0O0000O00O000O ,OO0O0OO000OOOO0O0 ,fontsize =2.6 ,text_thickness =3 ):#line:117
        (OO0O00OOOO00O0O0O ,O0O0O0O000O00O000 ),_OOO00O00OOOOO00O0 =cv2 .getTextSize (text =OOO0O0000O00O000O ,fontFace =cv2 .FONT_HERSHEY_DUPLEX ,fontScale =fontsize ,thickness =text_thickness )#line:119
        O00OOO0OOO000OO00 =O0000O0O0O0OOOOO0 .shape [1 ]//3 #line:120
        OO0O0OOOO00OO0O00 =O0O0O0O000O00O000 #line:121
        O000O00OOO0O0OO0O =O0O0O0O000O00O000 //5 #line:122
        cv2 .rectangle (O0000O0O0O0OOOOO0 ,(O00OOO0OOO000OO00 -O000O00OOO0O0OO0O *2 ,OO0O0OOOO00OO0O00 +O000O00OOO0O0OO0O ),(O00OOO0OOO000OO00 +OO0O00OOOO00O0O0O +O000O00OOO0O0OO0O *2 ,OO0O0OOOO00OO0O00 -O0O0O0O000O00O000 -O000O00OOO0O0OO0O ),(0 ,115 ,255 ),-1 )#line:124
        cv2 .putText (O0000O0O0O0OOOOO0 ,OOO0O0000O00O000O ,(O00OOO0OOO000OO00 ,OO0O0OOOO00OO0O00 ),cv2 .FONT_HERSHEY_DUPLEX ,fontsize ,(255 ,255 ,255 ),text_thickness )#line:128
        (OO0O00OOOO00O0O0O ,O0O0O0O000O00O000 ),_OOO00O00OOOOO00O0 =cv2 .getTextSize (text =OO0O0OO000OOOO0O0 ,fontFace =cv2 .FONT_HERSHEY_DUPLEX ,fontScale =fontsize ,thickness =text_thickness )#line:131
        O00OOO0OOO000OO00 =O00O0O00O0000O000 .shape [1 ]//3 #line:132
        OO0O0OOOO00OO0O00 =O0O0O0O000O00O000 #line:133
        O000O00OOO0O0OO0O =O0O0O0O000O00O000 //5 #line:134
        cv2 .rectangle (O00O0O00O0000O000 ,(O00OOO0OOO000OO00 -O000O00OOO0O0OO0O *2 ,OO0O0OOOO00OO0O00 +O000O00OOO0O0OO0O ),(O00OOO0OOO000OO00 +OO0O00OOOO00O0O0O +O000O00OOO0O0OO0O *2 ,OO0O0OOOO00OO0O00 -O0O0O0O000O00O000 -O000O00OOO0O0OO0O ),(94 ,23 ,235 ),-1 )#line:136
        cv2 .putText (O00O0O00O0000O000 ,OO0O0OO000OOOO0O0 ,(O00OOO0OOO000OO00 ,OO0O0OOOO00OO0O00 ),cv2 .FONT_HERSHEY_DUPLEX ,fontsize ,(255 ,255 ,255 ),text_thickness )#line:141
        O00OO0O000O00O000 =cv2 .hconcat ([O0000O0O0O0OOOOO0 ,O00O0O00O0000O000 ])#line:143
        if O00OO0O000O00O000 .shape [1 ]>3840 :#line:144
            O00OO0O000O00O000 =cv2 .resize (O00OO0O000O00O000 ,(3840 ,2160 ))#line:145
        return O00OO0O000O00O000 #line:147
class YOLOv8 :#line:152
    def __init__ (OOOO000OOO0OO00OO ,O0000O0O000OOO0O0 ,iConfThreshold =0.7 ,iIouThreshold =0.5 ):#line:154
        OOOO000OOO0OO00OO .confThreshold =iConfThreshold #line:155
        OOOO000OOO0OO00OO .iouThreshold =iIouThreshold #line:156
        OOOO000OOO0OO00OO .priInitModel (O0000O0O000OOO0O0 )#line:157
    def priInitModel (OO00000000O000OOO ,OOO0OO00OOO00O0OO ):#line:159
        OO00000000O000OOO .session =onnxruntime .InferenceSession (OOO0OO00OOO00O0OO ,providers =['CUDAExecutionProvider','CPUExecutionProvider'])#line:161
        OO00000000O000OOO .priGetInputDetails ()#line:162
        OO00000000O000OOO .priGetOutputDetails ()#line:163
    def priGetInputDetails (OOOO00OO0OO0OOO00 ):#line:165
        OO00O0OO00OO0O000 =OOOO00OO0OO0OOO00 .session .get_inputs ()#line:166
        OOOO00OO0OO0OOO00 .inputNames =[OO00O0OO00OO0O000 [O000OOO0000O00O00 ].name for O000OOO0000O00O00 in range (len (OO00O0OO00OO0O000 ))]#line:167
        OOOO00OO0OO0OOO00 .inputShape =OO00O0OO00OO0O000 [0 ].shape #line:168
        OOOO00OO0OO0OOO00 .inputHeight =OOOO00OO0OO0OOO00 .inputShape [2 ]#line:169
        OOOO00OO0OO0OOO00 .inputWidth =OOOO00OO0OO0OOO00 .inputShape [3 ]#line:170
    def priGetOutputDetails (OOOOOO000O0OOO000 ):#line:172
        OO00OO0O0OOO000O0 =OOOOOO000O0OOO000 .session .get_outputs ()#line:173
        OOOOOO000O0OOO000 .outputNames =[OO00OO0O0OOO000O0 [OO0OOO000O0OO0O00 ].name for OO0OOO000O0OO0O00 in range (len (OO00OO0O0OOO000O0 ))]#line:174
    def __call__ (OO00O0O00O00OO00O ,O0O0000OO0OO00O0O ):#line:176
        return OO00O0O00O00OO00O .priDetectObjects (O0O0000OO0OO00O0O )#line:177
    def priDetectObjects (OO0000O00OOO0O0OO ,OO0000O0O0O00OO00 ):#line:179
        O0000OOO0OO0OOOOO =OO0000O00OOO0O0OO .priPrepareInput (OO0000O0O0O00OO00 )#line:180
        O0000OOO0OOOO0O00 =OO0000O00OOO0O0OO .priInference (O0000OOO0OO0OOOOO )#line:181
        OO0000O00OOO0O0OO .boxes ,OO0000O00OOO0O0OO .scores ,OO0000O00OOO0O0OO .classIds =OO0000O00OOO0O0OO .priProcessOutput (O0000OOO0OOOO0O00 )#line:182
        return OO0000O00OOO0O0OO .boxes ,OO0000O00OOO0O0OO .scores ,OO0000O00OOO0O0OO .classIds #line:183
    def priPrepareInput (O0OO00OO0O00OOOO0 ,OO00O0O0OO0000OO0 ):#line:185
        O0OO00OO0O00OOOO0 .imgHeight ,O0OO00OO0O00OOOO0 .imgWidth =OO00O0O0OO0000OO0 .shape [:2 ]#line:186
        O000OOO00OO00000O =cv2 .cvtColor (OO00O0O0OO0000OO0 ,cv2 .COLOR_BGR2RGB )#line:188
        O000OOO00OO00000O =cv2 .resize (O000OOO00OO00000O ,(O0OO00OO0O00OOOO0 .inputWidth ,O0OO00OO0O00OOOO0 .inputHeight ))#line:191
        O000OOO00OO00000O =O000OOO00OO00000O /255.0 #line:194
        O000OOO00OO00000O =O000OOO00OO00000O .transpose (2 ,0 ,1 )#line:195
        OOOOOO0OO0O00O0OO =O000OOO00OO00000O [np .newaxis ,:,:,:].astype (np .float32 )#line:196
        return OOOOOO0OO0O00O0OO #line:198
    def priInference (OO0O00O00O000OOOO ,O0O0OO0O0OO0OO0OO ):#line:200
        OO0O0O000OO00OOO0 =time .perf_counter ()#line:201
        O00OO0OO0000O0OOO =OO0O00O00O000OOOO .session .run (OO0O00O00O000OOOO .outputNames ,{OO0O00O00O000OOOO .inputNames [0 ]:O0O0OO0O0OO0OO0OO })#line:202
        O0O00O00O0O000000 =time .perf_counter ()#line:203
        return O00OO0OO0000O0OOO #line:205
    def priProcessOutput (OOO00O0OO00O00000 ,O0O000O0OO0O000O0 ):#line:207
        OOO0O000OO0OOO0OO =np .squeeze (O0O000O0OO0O000O0 [0 ]).T #line:208
        O000O0OO0OOO0OO00 =np .max (OOO0O000OO0OOO0OO [:,4 :],axis =1 )#line:211
        OOO0O000OO0OOO0OO =OOO0O000OO0OOO0OO [O000O0OO0OOO0OO00 >OOO00O0OO00O00000 .confThreshold ,:]#line:212
        O000O0OO0OOO0OO00 =O000O0OO0OOO0OO00 [O000O0OO0OOO0OO00 >OOO00O0OO00O00000 .confThreshold ]#line:213
        if len (O000O0OO0OOO0OO00 )==0 :#line:215
            return [],[],[]#line:216
        O0O0000OOOOO0000O =np .argmax (OOO0O000OO0OOO0OO [:,4 :],axis =1 )#line:219
        O0OOO0OOOOOO0OOOO =OOO00O0OO00O00000 .priExtractBoxes (OOO0O000OO0OOO0OO )#line:222
        OO00OO000OO0O00OO =YoloUtils .nms (O0OOO0OOOOOO0OOOO ,O000O0OO0OOO0OO00 ,OOO00O0OO00O00000 .iouThreshold )#line:225
        return O0OOO0OOOOOO0OOOO [OO00OO000OO0O00OO ],O000O0OO0OOO0OO00 [OO00OO000OO0O00OO ],O0O0000OOOOO0000O [OO00OO000OO0O00OO ]#line:227
    def priExtractBoxes (OO0O00O0O0O00O0OO ,O0OO000O000O0O0OO ):#line:229
        O0000OOO000O000OO =O0OO000O000O0O0OO [:,:4 ]#line:231
        O0000OOO000O000OO =OO0O00O0O0O00O0OO .priRescaleBoxes (O0000OOO000O000OO )#line:234
        O0000OOO000O000OO =YoloUtils .xywh2xyxy (O0000OOO000O000OO )#line:237
        return O0000OOO000O000OO #line:239
    def priRescaleBoxes (OO0OO0OOO00OO0O00 ,OO0OO000O000O000O ):#line:241
        O0OOOOO0OO0O000OO =np .array ([OO0OO0OOO00OO0O00 .inputWidth ,OO0OO0OOO00OO0O00 .inputHeight ,OO0OO0OOO00OO0O00 .inputWidth ,OO0OO0OOO00OO0O00 .inputHeight ])#line:243
        OO0OO000O000O000O =np .divide (OO0OO000O000O000O ,O0OOOOO0OO0O000OO ,dtype =np .float32 )#line:244
        OO0OO000O000O000O *=np .array ([OO0OO0OOO00OO0O00 .imgWidth ,OO0OO0OOO00OO0O00 .imgHeight ,OO0OO0OOO00OO0O00 .imgWidth ,OO0OO0OOO00OO0O00 .imgHeight ])#line:245
        return OO0OO000O000O000O #line:246
    def drawDetections (O0000O0OO000000OO ,O00O00OO00OO0O0O0 ,bDrawScores =True ,iMaskAlpha =0.4 ):#line:249
        return YoloUtils .drawDetections (O00O00OO00OO0O0O0 ,O0000O0OO000000OO .boxes ,O0000O0OO000000OO .scores ,O0000O0OO000000OO .classIds ,iMaskAlpha )#line:250
if __name__ =='__main__':#line:253
    from imread_from_url import imread_from_url #line:254
    model_path ="../models/yolov8m.onnx"#line:256
    yolov7_detector =YOLOv8 (model_path ,iConfThreshold =0.3 ,iIouThreshold =0.5 )#line:259
    img_url ="https://live.staticflickr.com/13/19041780_d6fd803de0_3k.jpg"#line:261
    img =imread_from_url (img_url )#line:262
    yolov7_detector (img )#line:265
    combined_img =yolov7_detector .drawDetections (img )#line:268
    cv2 .namedWindow ("Output",cv2 .WINDOW_NORMAL )#line:269
    cv2 .imshow ("Output",combined_img )#line:270
    cv2 .waitKey (0 )#line:271
