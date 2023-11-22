import time #line:1
import cv2 #line:2
import numpy as np #line:3
import onnxruntime #line:4
class_names =['person','bicycle','car','motorcycle','airplane','bus','train','truck','boat','traffic light','fire hydrant','stop sign','parking meter','bench','bird','cat','dog','horse','sheep','cow','elephant','bear','zebra','giraffe','backpack','umbrella','handbag','tie','suitcase','frisbee','skis','snowboard','sports ball','kite','baseball bat','baseball glove','skateboard','surfboard','tennis racket','bottle','wine glass','cup','fork','knife','spoon','bowl','banana','apple','sandwich','orange','broccoli','carrot','hot dog','pizza','donut','cake','chair','couch','potted plant','bed','dining table','toilet','tv','laptop','mouse','remote','keyboard','cell phone','microwave','oven','toaster','sink','refrigerator','book','clock','vase','scissors','teddy bear','hair drier','toothbrush']#line:14
rng =np .random .default_rng (3 )#line:17
colors =rng .uniform (0 ,255 ,size =(len (class_names ),3 ))#line:18
class YoloUtils :#line:21
    @staticmethod #line:22
    def nms (OOO0OO00000O000OO ,OO00O0OOO0000OOOO ,OO0O00O0OOOO0OOO0 ):#line:23
        OO0OO00O0OOO000O0 =np .argsort (OO00O0OOO0000OOOO )[::-1 ]#line:25
        O0OO0O0000OOOOOOO =[]#line:27
        while OO0OO00O0OOO000O0 .size >0 :#line:28
            OOOOOO000OO0O0OO0 =OO0OO00O0OOO000O0 [0 ]#line:30
            O0OO0O0000OOOOOOO .append (OOOOOO000OO0O0OO0 )#line:31
            O0O0OO0O0OOOOO0O0 =YoloUtils .compute_iou (OOO0OO00000O000OO [OOOOOO000OO0O0OO0 ,:],OOO0OO00000O000OO [OO0OO00O0OOO000O0 [1 :],:])#line:34
            OOOOO0OO0OOOOOO00 =np .where (O0O0OO0O0OOOOO0O0 <OO0O00O0OOOO0OOO0 )[0 ]#line:37
            OO0OO00O0OOO000O0 =OO0OO00O0OOO000O0 [OOOOO0OO0OOOOOO00 +1 ]#line:40
        return O0OO0O0000OOOOOOO #line:42
    @staticmethod #line:44
    def compute_iou (OOO0O00O00OOOOOOO ,O00O0O00O0000O0O0 ):#line:46
        OOO0OO0000O0O0O0O =np .maximum (OOO0O00O00OOOOOOO [0 ],O00O0O00O0000O0O0 [:,0 ])#line:48
        OO0O000O000OOO000 =np .maximum (OOO0O00O00OOOOOOO [1 ],O00O0O00O0000O0O0 [:,1 ])#line:49
        OOOO0000OO0OOOO0O =np .minimum (OOO0O00O00OOOOOOO [2 ],O00O0O00O0000O0O0 [:,2 ])#line:50
        OOO00OO0OO0O0O0O0 =np .minimum (OOO0O00O00OOOOOOO [3 ],O00O0O00O0000O0O0 [:,3 ])#line:51
        OOO0O00OOO0O00000 =np .maximum (0 ,OOOO0000OO0OOOO0O -OOO0OO0000O0O0O0O )*np .maximum (0 ,OOO00OO0OO0O0O0O0 -OO0O000O000OOO000 )#line:54
        O0OO0OO0O00O000OO =(OOO0O00O00OOOOOOO [2 ]-OOO0O00O00OOOOOOO [0 ])*(OOO0O00O00OOOOOOO [3 ]-OOO0O00O00OOOOOOO [1 ])#line:57
        OO0OOOOOO0O00OO0O =(O00O0O00O0000O0O0 [:,2 ]-O00O0O00O0000O0O0 [:,0 ])*(O00O0O00O0000O0O0 [:,3 ]-O00O0O00O0000O0O0 [:,1 ])#line:58
        OOO00OOOOOO00000O =O0OO0OO0O00O000OO +OO0OOOOOO0O00OO0O -OOO0O00OOO0O00000 #line:59
        O0OO0O0OOOOO0OOOO =OOO0O00OOO0O00000 /OOO00OOOOOO00000O #line:62
        return O0OO0O0OOOOO0OOOO #line:64
    @staticmethod #line:66
    def xywh2xyxy (O0OOO000O0OOOOO0O ):#line:68
        O00OOO0OO0O00000O =np .copy (O0OOO000O0OOOOO0O )#line:70
        O00OOO0OO0O00000O [...,0 ]=O0OOO000O0OOOOO0O [...,0 ]-O0OOO000O0OOOOO0O [...,2 ]/2 #line:71
        O00OOO0OO0O00000O [...,1 ]=O0OOO000O0OOOOO0O [...,1 ]-O0OOO000O0OOOOO0O [...,3 ]/2 #line:72
        O00OOO0OO0O00000O [...,2 ]=O0OOO000O0OOOOO0O [...,0 ]+O0OOO000O0OOOOO0O [...,2 ]/2 #line:73
        O00OOO0OO0O00000O [...,3 ]=O0OOO000O0OOOOO0O [...,1 ]+O0OOO000O0OOOOO0O [...,3 ]/2 #line:74
        return O00OOO0OO0O00000O #line:75
    @staticmethod #line:77
    def drawDetections (O00O0O000OOO00OOO ,OOOOO0OO0000000O0 ,OOO00OO0O0O0OO000 ,OOO0OOO0O000O0O00 ,mask_alpha =0.3 ):#line:78
        O00OOO0O0OOO0O0O0 =O00O0O000OOO00OOO .copy ()#line:79
        OO00000OO0000O0O0 =O00O0O000OOO00OOO .copy ()#line:80
        OO0O00O00OOOOO0O0 ,O00O00OOOOO0000OO =O00O0O000OOO00OOO .shape [:2 ]#line:82
        O0OOOOOOO000O0OOO =min ([OO0O00O00OOOOO0O0 ,O00O00OOOOO0000OO ])*0.0006 #line:83
        OOO00000000000O00 =int (min ([OO0O00O00OOOOO0O0 ,O00O00OOOOO0000OO ])*0.001 )#line:84
        for OO00000000O000O00 ,OO00OO000OOOOO000 ,O0O0000O0OOOOO00O in zip (OOOOO0OO0000000O0 ,OOO00OO0O0O0OO000 ,OOO0OOO0O000O0O00 ):#line:87
            O00OO0OO0O0O0O0O0 =colors [O0O0000O0OOOOO00O ]#line:88
            OOOO0O0O00OOO0O00 ,OOOOOO0000OOOOOOO ,OO000OO00O0OO0OOO ,OO0OO0O0O00OO0000 =OO00000000O000O00 .astype (int )#line:90
            cv2 .rectangle (OO00000OO0000O0O0 ,(OOOO0O0O00OOO0O00 ,OOOOOO0000OOOOOOO ),(OO000OO00O0OO0OOO ,OO0OO0O0O00OO0000 ),O00OO0OO0O0O0O0O0 ,2 )#line:93
            cv2 .rectangle (O00OOO0O0OOO0O0O0 ,(OOOO0O0O00OOO0O00 ,OOOOOO0000OOOOOOO ),(OO000OO00O0OO0OOO ,OO0OO0O0O00OO0000 ),O00OO0OO0O0O0O0O0 ,-1 )#line:96
            OOOO000O000OO0000 =class_names [O0O0000O0OOOOO00O ]#line:98
            OOOO0OOOOO0OOO00O =f'{OOOO000O000OO0000} {int(OO00OO000OOOOO000 * 100)}%'#line:99
            (O0OO0O0OO0OOO0000 ,O00000O0OO00OOO0O ),_OOOOOO0OOO000OO0O =cv2 .getTextSize (text =OOOO0OOOOO0OOO00O ,fontFace =cv2 .FONT_HERSHEY_SIMPLEX ,fontScale =O0OOOOOOO000O0OOO ,thickness =OOO00000000000O00 )#line:101
            O00000O0OO00OOO0O =int (O00000O0OO00OOO0O *1.2 )#line:102
            cv2 .rectangle (OO00000OO0000O0O0 ,(OOOO0O0O00OOO0O00 ,OOOOOO0000OOOOOOO ),(OOOO0O0O00OOO0O00 +O0OO0O0OO0OOO0000 ,OOOOOO0000OOOOOOO -O00000O0OO00OOO0O ),O00OO0OO0O0O0O0O0 ,-1 )#line:105
            cv2 .rectangle (O00OOO0O0OOO0O0O0 ,(OOOO0O0O00OOO0O00 ,OOOOOO0000OOOOOOO ),(OOOO0O0O00OOO0O00 +O0OO0O0OO0OOO0000 ,OOOOOO0000OOOOOOO -O00000O0OO00OOO0O ),O00OO0OO0O0O0O0O0 ,-1 )#line:107
            cv2 .putText (OO00000OO0000O0O0 ,OOOO0OOOOO0OOO00O ,(OOOO0O0O00OOO0O00 ,OOOOOO0000OOOOOOO ),cv2 .FONT_HERSHEY_SIMPLEX ,O0OOOOOOO000O0OOO ,(255 ,255 ,255 ),OOO00000000000O00 ,cv2 .LINE_AA )#line:109
            cv2 .putText (O00OOO0O0OOO0O0O0 ,OOOO0OOOOO0OOO00O ,(OOOO0O0O00OOO0O00 ,OOOOOO0000OOOOOOO ),cv2 .FONT_HERSHEY_SIMPLEX ,O0OOOOOOO000O0OOO ,(255 ,255 ,255 ),OOO00000000000O00 ,cv2 .LINE_AA )#line:112
        return cv2 .addWeighted (O00OOO0O0OOO0O0O0 ,mask_alpha ,OO00000OO0000O0O0 ,1 -mask_alpha ,0 )#line:114
    @staticmethod #line:116
    def draw_comparison (OOO0OO0O00O0000O0 ,OO00O0O0O0O0O00O0 ,OO0O00000O0OO0O00 ,OOOO000O00O000000 ,fontsize =2.6 ,text_thickness =3 ):#line:117
        (O0OO0O00OO0O00OOO ,O0O0O0O0000OO0000 ),_OO0OO0OOO000OOOOO =cv2 .getTextSize (text =OO0O00000O0OO0O00 ,fontFace =cv2 .FONT_HERSHEY_DUPLEX ,fontScale =fontsize ,thickness =text_thickness )#line:119
        OOOO0O0O0000O00OO =OOO0OO0O00O0000O0 .shape [1 ]//3 #line:120
        O0OOO0OOO000OOOO0 =O0O0O0O0000OO0000 #line:121
        O0O00OO00O000OO00 =O0O0O0O0000OO0000 //5 #line:122
        cv2 .rectangle (OOO0OO0O00O0000O0 ,(OOOO0O0O0000O00OO -O0O00OO00O000OO00 *2 ,O0OOO0OOO000OOOO0 +O0O00OO00O000OO00 ),(OOOO0O0O0000O00OO +O0OO0O00OO0O00OOO +O0O00OO00O000OO00 *2 ,O0OOO0OOO000OOOO0 -O0O0O0O0000OO0000 -O0O00OO00O000OO00 ),(0 ,115 ,255 ),-1 )#line:124
        cv2 .putText (OOO0OO0O00O0000O0 ,OO0O00000O0OO0O00 ,(OOOO0O0O0000O00OO ,O0OOO0OOO000OOOO0 ),cv2 .FONT_HERSHEY_DUPLEX ,fontsize ,(255 ,255 ,255 ),text_thickness )#line:128
        (O0OO0O00OO0O00OOO ,O0O0O0O0000OO0000 ),_OO0OO0OOO000OOOOO =cv2 .getTextSize (text =OOOO000O00O000000 ,fontFace =cv2 .FONT_HERSHEY_DUPLEX ,fontScale =fontsize ,thickness =text_thickness )#line:131
        OOOO0O0O0000O00OO =OO00O0O0O0O0O00O0 .shape [1 ]//3 #line:132
        O0OOO0OOO000OOOO0 =O0O0O0O0000OO0000 #line:133
        O0O00OO00O000OO00 =O0O0O0O0000OO0000 //5 #line:134
        cv2 .rectangle (OO00O0O0O0O0O00O0 ,(OOOO0O0O0000O00OO -O0O00OO00O000OO00 *2 ,O0OOO0OOO000OOOO0 +O0O00OO00O000OO00 ),(OOOO0O0O0000O00OO +O0OO0O00OO0O00OOO +O0O00OO00O000OO00 *2 ,O0OOO0OOO000OOOO0 -O0O0O0O0000OO0000 -O0O00OO00O000OO00 ),(94 ,23 ,235 ),-1 )#line:136
        cv2 .putText (OO00O0O0O0O0O00O0 ,OOOO000O00O000000 ,(OOOO0O0O0000O00OO ,O0OOO0OOO000OOOO0 ),cv2 .FONT_HERSHEY_DUPLEX ,fontsize ,(255 ,255 ,255 ),text_thickness )#line:141
        O0000OOO0OO0OOO0O =cv2 .hconcat ([OOO0OO0O00O0000O0 ,OO00O0O0O0O0O00O0 ])#line:143
        if O0000OOO0OO0OOO0O .shape [1 ]>3840 :#line:144
            O0000OOO0OO0OOO0O =cv2 .resize (O0000OOO0OO0OOO0O ,(3840 ,2160 ))#line:145
        return O0000OOO0OO0OOO0O #line:147
class YOLOv8 :#line:152
    def __init__ (OOOO0000O0OO00O00 ,O00OOO0OOO00OO00O ,iConfThreshold =0.7 ,iIouThreshold =0.5 ):#line:154
        OOOO0000O0OO00O00 .confThreshold =iConfThreshold #line:155
        OOOO0000O0OO00O00 .iouThreshold =iIouThreshold #line:156
        OOOO0000O0OO00O00 .priInitModel (O00OOO0OOO00OO00O )#line:157
    def priInitModel (O0O0O0O0OO000O0OO ,OOO0O00O00O00O0O0 ):#line:159
        O0O0O0O0OO000O0OO .session =onnxruntime .InferenceSession (OOO0O00O00O00O0O0 ,providers =['CUDAExecutionProvider','CPUExecutionProvider'])#line:161
        O0O0O0O0OO000O0OO .priGetInputDetails ()#line:162
        O0O0O0O0OO000O0OO .priGetOutputDetails ()#line:163
    def priGetInputDetails (O00O0OO00OO0000O0 ):#line:165
        OO00O0OOO0OO0OOO0 =O00O0OO00OO0000O0 .session .get_inputs ()#line:166
        O00O0OO00OO0000O0 .inputNames =[OO00O0OOO0OO0OOO0 [O0OOOOOOOO0O00O00 ].name for O0OOOOOOOO0O00O00 in range (len (OO00O0OOO0OO0OOO0 ))]#line:167
        O00O0OO00OO0000O0 .inputShape =OO00O0OOO0OO0OOO0 [0 ].shape #line:168
        O00O0OO00OO0000O0 .inputHeight =O00O0OO00OO0000O0 .inputShape [2 ]#line:169
        O00O0OO00OO0000O0 .inputWidth =O00O0OO00OO0000O0 .inputShape [3 ]#line:170
    def priGetOutputDetails (O000OOOO00OOO0OO0 ):#line:172
        O00O00000OOOOO0OO =O000OOOO00OOO0OO0 .session .get_outputs ()#line:173
        O000OOOO00OOO0OO0 .outputNames =[O00O00000OOOOO0OO [O0O00O000000O0000 ].name for O0O00O000000O0000 in range (len (O00O00000OOOOO0OO ))]#line:174
    def __call__ (OO0OOO0OO0OO00OOO ,O0OO0O0000O00O0OO ):#line:176
        return OO0OOO0OO0OO00OOO .priDetectObjects (O0OO0O0000O00O0OO )#line:177
    def priDetectObjects (O00000O0OOOO0O0OO ,O0O0O0O00000000O0 ):#line:179
        OO0OO0O00OO00OOOO =O00000O0OOOO0O0OO .priPrepareInput (O0O0O0O00000000O0 )#line:180
        O0OO00O0000OOOO00 =O00000O0OOOO0O0OO .priInference (OO0OO0O00OO00OOOO )#line:181
        O00000O0OOOO0O0OO .boxes ,O00000O0OOOO0O0OO .scores ,O00000O0OOOO0O0OO .classIds =O00000O0OOOO0O0OO .priProcessOutput (O0OO00O0000OOOO00 )#line:182
        return O00000O0OOOO0O0OO .boxes ,O00000O0OOOO0O0OO .scores ,O00000O0OOOO0O0OO .classIds #line:183
    def priPrepareInput (O0OO000000OO0OO00 ,O0O0OOO000O00OOO0 ):#line:185
        O0OO000000OO0OO00 .imgHeight ,O0OO000000OO0OO00 .imgWidth =O0O0OOO000O00OOO0 .shape [:2 ]#line:186
        OO0000O0O0OO0O00O =cv2 .cvtColor (O0O0OOO000O00OOO0 ,cv2 .COLOR_BGR2RGB )#line:188
        OO0000O0O0OO0O00O =cv2 .resize (OO0000O0O0OO0O00O ,(O0OO000000OO0OO00 .inputWidth ,O0OO000000OO0OO00 .inputHeight ))#line:191
        OO0000O0O0OO0O00O =OO0000O0O0OO0O00O /255.0 #line:194
        OO0000O0O0OO0O00O =OO0000O0O0OO0O00O .transpose (2 ,0 ,1 )#line:195
        OOOOOOOOOO00O00O0 =OO0000O0O0OO0O00O [np .newaxis ,:,:,:].astype (np .float32 )#line:196
        return OOOOOOOOOO00O00O0 #line:198
    def priInference (O0OO0OO00OO00OO0O ,O00000000O000O0OO ):#line:200
        O000OO0OO0O0OO000 =time .perf_counter ()#line:201
        OO0O00000OO0000OO =O0OO0OO00OO00OO0O .session .run (O0OO0OO00OO00OO0O .outputNames ,{O0OO0OO00OO00OO0O .inputNames [0 ]:O00000000O000O0OO })#line:202
        O00O00OOO0000O0OO =time .perf_counter ()#line:203
        return OO0O00000OO0000OO #line:205
    def priProcessOutput (OO000OOOO0O00O0O0 ,O000O0O0OO0OO00OO ):#line:207
        OO0OO000O00O0OOOO =np .squeeze (O000O0O0OO0OO00OO [0 ]).T #line:208
        O000O00O0OOO000OO =np .max (OO0OO000O00O0OOOO [:,4 :],axis =1 )#line:211
        OO0OO000O00O0OOOO =OO0OO000O00O0OOOO [O000O00O0OOO000OO >OO000OOOO0O00O0O0 .confThreshold ,:]#line:212
        O000O00O0OOO000OO =O000O00O0OOO000OO [O000O00O0OOO000OO >OO000OOOO0O00O0O0 .confThreshold ]#line:213
        if len (O000O00O0OOO000OO )==0 :#line:215
            return [],[],[]#line:216
        O00O0O0O0OO0O0OO0 =np .argmax (OO0OO000O00O0OOOO [:,4 :],axis =1 )#line:219
        OO00O0000O0O00O0O =OO000OOOO0O00O0O0 .priExtractBoxes (OO0OO000O00O0OOOO )#line:222
        OOO00O0OO000OO0O0 =YoloUtils .nms (OO00O0000O0O00O0O ,O000O00O0OOO000OO ,OO000OOOO0O00O0O0 .iouThreshold )#line:225
        return OO00O0000O0O00O0O [OOO00O0OO000OO0O0 ],O000O00O0OOO000OO [OOO00O0OO000OO0O0 ],O00O0O0O0OO0O0OO0 [OOO00O0OO000OO0O0 ]#line:227
    def priExtractBoxes (O00OO00000OO0O0OO ,O00O0O000O0OOOO0O ):#line:229
        O0O0OO00OO0OO0000 =O00O0O000O0OOOO0O [:,:4 ]#line:231
        O0O0OO00OO0OO0000 =O00OO00000OO0O0OO .priRescaleBoxes (O0O0OO00OO0OO0000 )#line:234
        O0O0OO00OO0OO0000 =YoloUtils .xywh2xyxy (O0O0OO00OO0OO0000 )#line:237
        return O0O0OO00OO0OO0000 #line:239
    def priRescaleBoxes (O000O000000000O0O ,OOO0OO0O000000OO0 ):#line:241
        OOOOO000OOO00O0OO =np .array ([O000O000000000O0O .inputWidth ,O000O000000000O0O .inputHeight ,O000O000000000O0O .inputWidth ,O000O000000000O0O .inputHeight ])#line:243
        OOO0OO0O000000OO0 =np .divide (OOO0OO0O000000OO0 ,OOOOO000OOO00O0OO ,dtype =np .float32 )#line:244
        OOO0OO0O000000OO0 *=np .array ([O000O000000000O0O .imgWidth ,O000O000000000O0O .imgHeight ,O000O000000000O0O .imgWidth ,O000O000000000O0O .imgHeight ])#line:245
        return OOO0OO0O000000OO0 #line:246
    def drawDetections (O0O00O0O000O0O000 ,O000OO00OO0OO00O0 ,bDrawScores =True ,iMaskAlpha =0.4 ):#line:249
        return YoloUtils .drawDetections (O000OO00OO0OO00O0 ,O0O00O0O000O0O000 .boxes ,O0O00O0O000O0O000 .scores ,O0O00O0O000O0O000 .classIds ,iMaskAlpha )#line:250
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
