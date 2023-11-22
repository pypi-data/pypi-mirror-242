from loguru import logger #line:1
import os #line:2
import sys #line:3
sys .path .append (os .getcwd ())#line:5
TEMPLATE_FILE_LOG ="[{0}]{1}"#line:7
"""日志模板"""#line:8
class LogUtilsEx :#line:11
    ""#line:12
    def __init__ (O00000OOO000OO0OO ):#line:14
        ""#line:15
        O00000OOO000OO0OO .logFilterVoList =[]#line:17
        O00000OOO000OO0OO .logger =logger #line:20
    def init (OO00O00OO0O0O000O ,dirPathRelativeConf ="",bDebug =False ,fileNameLog ="app.log",logRotationTime ="02:00"):#line:23
        ""#line:31
        O0000OO0OO00O0OO0 =dirPathRelativeConf +"resources/logs"#line:33
        if not os .path .exists (O0000OO0OO00O0OO0 ):#line:34
            os .makedirs (O0000OO0OO00O0OO0 )#line:35
        OO00000O00O00O0O0 =os .path .join (O0000OO0OO00O0OO0 ,fileNameLog )#line:36
        OO00O00OO0O0O000O .priInitLogFilterKeyVoList (dirPathRelativeConf )#line:39
        logger .remove ()#line:42
        OOO0O0OO00O0OOOOO ="DEBUG"if bDebug else "INFO"#line:45
        logger .add (sys .stdout ,level =OOO0O0OO00O0OOOOO )#line:46
        logger .add (OO00000O00O00O0O0 ,rotation =logRotationTime ,level =OOO0O0OO00O0OOOOO )#line:47
    def debug (O00O0OOOOO0OO0O0O ,OO000O0OO0000OOOO ,OOO0OO0OO0O0O0OOO ,logFilterKey =""):#line:49
        ""#line:56
        OOOOOO0OO0OO0O000 =O00O0OOOOO0OO0O0O .priGetLogFilterVo (logFilterKey )#line:57
        if OOOOOO0OO0OO0O000 is not None and OOOOOO0OO0OO0O000 .open is False :#line:58
            return #line:59
        LOG .logger .debug (TEMPLATE_FILE_LOG .format (OO000O0OO0000OOOO ,OOO0OO0OO0O0O0OOO ))#line:60
    def info (OOO00O0000OO0OOOO ,OOOO0O0000OO0OO00 ,O00OOOOOOO0O0O000 ,logFilterKey =""):#line:62
        ""#line:69
        O00O00OO0O0O0OOO0 =OOO00O0000OO0OOOO .priGetLogFilterVo (logFilterKey )#line:70
        if O00O00OO0O0O0OOO0 is not None and O00O00OO0O0O0OOO0 .open is False :#line:71
            return #line:72
        LOG .logger .info (TEMPLATE_FILE_LOG .format (OOOO0O0000OO0OO00 ,O00OOOOOOO0O0O000 ))#line:73
    def warn (OOOOOO0O00OOO0OOO ,O000OOO00O0OOO0O0 ,OO000O000OO00OO0O ,logFilterKey =""):#line:75
        ""#line:82
        O0O00OO0O0O00OO00 =OOOOOO0O00OOO0OOO .priGetLogFilterVo (logFilterKey )#line:83
        if O0O00OO0O0O00OO00 is not None and O0O00OO0O0O00OO00 .open is False :#line:84
            return #line:85
        LOG .logger .warning (TEMPLATE_FILE_LOG .format (O000OOO00O0OOO0O0 ,OO000O000OO00OO0O ))#line:86
    def error (O0O000O00OO0OO0OO ,O000OO0O00O0OOO0O ,O00000O0OO0OOOOO0 ,logFilterKey =""):#line:88
        ""#line:95
        OO000OO0OO0O000OO =O0O000O00OO0OO0OO .priGetLogFilterVo (logFilterKey )#line:96
        if OO000OO0OO0O000OO is not None and OO000OO0OO0O000OO .open is False :#line:97
            return #line:98
        LOG .logger .error (TEMPLATE_FILE_LOG .format (O000OO0O00O0OOO0O ,O00000O0OO0OOOOO0 ))#line:99
    def priInitLogFilterKeyVoList (OOOO000OO00OO0O0O ,O0OOOO00O0O0O0OOO ):#line:101
        OOOO000OO00OO0O0O .logFilterVoList =[]#line:102
        for OO0OOOO0OOOOO00O0 in open (O0OOOO00O0O0O0OOO +"resources/logFilter.txt",encoding ="utf-8"):#line:104
            O000OO0O0OOOO0000 =OO0OOOO0OOOOO00O0 .replace ("\n","").split (",")#line:105
            if len (O000OO0O0OOOO0000 )==3 :#line:106
                OOOOO00OO0O0O0000 =O000OO0O0OOOO0000 [0 ]#line:107
                O00OO0O00OOOO0000 =False if O000OO0O0OOOO0000 [1 ]=="-"else True #line:108
                O0OO0O0OOO0O000OO =True if O000OO0O0OOOO0000 [2 ]=="A"else False #line:109
                OOOO000OO00OO0O0O .logFilterVoList .append (LogFilterVo (OOOOO00OO0O0O0000 ,O00OO0O00OOOO0000 ,O0OO0O0OOO0O000OO ))#line:110
        return 1 #line:112
    def priGetLogFilterVo (O0O00O0OO0O0OO000 ,O00OOOO0000OO0O00 ):#line:114
        for O0O00OO000O0O0O0O ,OOO0OO0OO0OOOO0O0 in enumerate (O0O00O0OO0O0OO000 .logFilterVoList ):#line:115
            if OOO0OO0OO0OOOO0O0 .logFilterKey ==O00OOOO0000OO0O00 :#line:116
                return OOO0OO0OO0OOOO0O0 #line:117
        return None #line:118
class LogFilterVo :#line:121
    ""#line:122
    def __init__ (O0O0OOOOOO000O00O ,OOOO000O0O0OOOO00 ,bOpen =False ,full =True ):#line:124
        ""#line:130
        O0O0OOOOOO000O00O .logFilterKey =OOOO000O0O0OOOO00 #line:131
        O0O0OOOOOO000O00O .open =bOpen #line:132
        O0O0OOOOOO000O00O .full =full #line:133
LOG =LogUtilsEx ()#line:136
"""日志对象"""#line:137
if __name__ =="__main__":#line:141
    LOG .init ("../../../appqa/",True )#line:142
    LOG .debug ("WpRun","日志测试1...","调度器-L1-mesInit")#line:143
    LOG .info ("WpRun","日志测试2...","调度器-L1-mesInit")#line:144
    LOG .warn ("WpRun","日志测试3...","调度器-L1-mesInit")#line:145
    LOG .error ("WpRun","日志测试4...","调度器-L1-mesInit")#line:146
