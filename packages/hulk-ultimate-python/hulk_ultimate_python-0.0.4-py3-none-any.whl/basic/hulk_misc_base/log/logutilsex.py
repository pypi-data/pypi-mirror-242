from loguru import logger #line:1
import os #line:2
import sys #line:3
sys .path .append (os .getcwd ())#line:5
TEMPLATE_FILE_LOG ="[{0}]{1}"#line:7
"""日志模板"""#line:8
class LogUtilsEx :#line:11
    ""#line:12
    def __init__ (O0000O0O00000O000 ):#line:14
        ""#line:15
        O0000O0O00000O000 .logFilterVoList =[]#line:17
        O0000O0O00000O000 .logger =logger #line:20
    def init (OOOO0OO00OO0O0OO0 ,dirPathRelativeConf ="",bDebug =False ,fileNameLog ="app.log",logRotationTime ="02:00"):#line:23
        ""#line:31
        O0O000OO0000O000O =dirPathRelativeConf +"resources/logs"#line:33
        if not os .path .exists (O0O000OO0000O000O ):#line:34
            os .makedirs (O0O000OO0000O000O )#line:35
        OOO0O00000000O0O0 =os .path .join (O0O000OO0000O000O ,fileNameLog )#line:36
        OOOO0OO00OO0O0OO0 .priInitLogFilterKeyVoList (dirPathRelativeConf )#line:39
        logger .remove ()#line:42
        OOOOOO000OO000000 ="DEBUG"if bDebug else "INFO"#line:45
        logger .add (sys .stdout ,level =OOOOOO000OO000000 )#line:46
        logger .add (OOO0O00000000O0O0 ,rotation =logRotationTime ,level =OOOOOO000OO000000 )#line:47
    def debug (OOO0OO0000O0O0O00 ,OOOO00OO0O00O00OO ,OO00O0OO00OOO0O0O ,logFilterKey =""):#line:49
        ""#line:56
        OOO00OOO00O00OO00 =OOO0OO0000O0O0O00 .priGetLogFilterVo (logFilterKey )#line:57
        if OOO00OOO00O00OO00 is not None and OOO00OOO00O00OO00 .open is False :#line:58
            return #line:59
        LOG .logger .debug (TEMPLATE_FILE_LOG .format (OOOO00OO0O00O00OO ,OO00O0OO00OOO0O0O ))#line:60
    def info (OO0O00O000O00OOO0 ,O0000000O000O0000 ,OOOOOO00O0OOO0OO0 ,logFilterKey =""):#line:62
        ""#line:69
        OO0O00O000OO000OO =OO0O00O000O00OOO0 .priGetLogFilterVo (logFilterKey )#line:70
        if OO0O00O000OO000OO is not None and OO0O00O000OO000OO .open is False :#line:71
            return #line:72
        LOG .logger .info (TEMPLATE_FILE_LOG .format (O0000000O000O0000 ,OOOOOO00O0OOO0OO0 ))#line:73
    def warn (O00OO00OO000OO0O0 ,OOOOOOOOO00OOOOOO ,OOO00OOOO0OOOO000 ,logFilterKey =""):#line:75
        ""#line:82
        OOO00000O00OOO00O =O00OO00OO000OO0O0 .priGetLogFilterVo (logFilterKey )#line:83
        if OOO00000O00OOO00O is not None and OOO00000O00OOO00O .open is False :#line:84
            return #line:85
        LOG .logger .warning (TEMPLATE_FILE_LOG .format (OOOOOOOOO00OOOOOO ,OOO00OOOO0OOOO000 ))#line:86
    def error (O00OOO0O000O0O0OO ,OOO0O0OOOO0OOO00O ,OO0OO000O0000O000 ,logFilterKey =""):#line:88
        ""#line:95
        OO00O00O0OO000OO0 =O00OOO0O000O0O0OO .priGetLogFilterVo (logFilterKey )#line:96
        if OO00O00O0OO000OO0 is not None and OO00O00O0OO000OO0 .open is False :#line:97
            return #line:98
        LOG .logger .error (TEMPLATE_FILE_LOG .format (OOO0O0OOOO0OOO00O ,OO0OO000O0000O000 ))#line:99
    def priInitLogFilterKeyVoList (O00O0O0OOOO00O000 ,O000OO00OO0O0000O ):#line:101
        O00O0O0OOOO00O000 .logFilterVoList =[]#line:102
        for OOO0O000OO0O0O000 in open (O000OO00OO0O0000O +"resources/logFilter.txt",encoding ="utf-8"):#line:104
            OO000O000O000OOO0 =OOO0O000OO0O0O000 .replace ("\n","").split (",")#line:105
            if len (OO000O000O000OOO0 )==3 :#line:106
                O000OO00OOO000O00 =OO000O000O000OOO0 [0 ]#line:107
                O00OO0O00OO000000 =False if OO000O000O000OOO0 [1 ]=="-"else True #line:108
                OOO0O000O0000O0O0 =True if OO000O000O000OOO0 [2 ]=="A"else False #line:109
                O00O0O0OOOO00O000 .logFilterVoList .append (LogFilterVo (O000OO00OOO000O00 ,O00OO0O00OO000000 ,OOO0O000O0000O0O0 ))#line:110
        return 1 #line:112
    def priGetLogFilterVo (OOOOO0OO0O0OOOO00 ,OO00OOO00OOOO0OO0 ):#line:114
        for OO000000O0OOO0OOO ,OOO000000OOOOO000 in enumerate (OOOOO0OO0O0OOOO00 .logFilterVoList ):#line:115
            if OOO000000OOOOO000 .logFilterKey ==OO00OOO00OOOO0OO0 :#line:116
                return OOO000000OOOOO000 #line:117
        return None #line:118
class LogFilterVo :#line:121
    ""#line:122
    def __init__ (OOOO0000O00O00O00 ,O00OO00000O0OOOOO ,bOpen =False ,full =True ):#line:124
        ""#line:130
        OOOO0000O00O00O00 .logFilterKey =O00OO00000O0OOOOO #line:131
        OOOO0000O00O00O00 .open =bOpen #line:132
        OOOO0000O00O00O00 .full =full #line:133
LOG =LogUtilsEx ()#line:136
"""日志对象"""#line:137
if __name__ =="__main__":#line:141
    LOG .init ("../../../appqa/",True )#line:142
    LOG .debug ("WpRun","日志测试1...","调度器-L1-mesInit")#line:143
    LOG .info ("WpRun","日志测试2...","调度器-L1-mesInit")#line:144
    LOG .warn ("WpRun","日志测试3...","调度器-L1-mesInit")#line:145
    LOG .error ("WpRun","日志测试4...","调度器-L1-mesInit")#line:146
