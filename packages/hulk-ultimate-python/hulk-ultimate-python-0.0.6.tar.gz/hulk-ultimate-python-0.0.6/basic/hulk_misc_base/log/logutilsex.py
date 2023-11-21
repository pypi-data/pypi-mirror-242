from loguru import logger #line:1
import os #line:2
import sys #line:3
sys .path .append (os .getcwd ())#line:5
TEMPLATE_FILE_LOG ="[{0}]{1}"#line:7
"""日志模板"""#line:8
class LogUtilsEx :#line:11
    ""#line:12
    def __init__ (O00OO0OO00OO0000O ):#line:14
        ""#line:15
        O00OO0OO00OO0000O .logFilterVoList =[]#line:17
        O00OO0OO00OO0000O .logger =logger #line:20
    def init (OO0OO00OOO0OOO0OO ,dirPathRelativeConf ="",bDebug =False ,fileNameLog ="app.log",logRotationTime ="02:00"):#line:23
        ""#line:31
        OOOOO0O00OOOOO0OO =dirPathRelativeConf +"resources/logs"#line:33
        if not os .path .exists (OOOOO0O00OOOOO0OO ):#line:34
            os .makedirs (OOOOO0O00OOOOO0OO )#line:35
        OOO00OO00OOOO0O0O =os .path .join (OOOOO0O00OOOOO0OO ,fileNameLog )#line:36
        OO0OO00OOO0OOO0OO .priInitLogFilterKeyVoList (dirPathRelativeConf )#line:39
        logger .remove ()#line:42
        O00OO00OOO000OOO0 ="DEBUG"if bDebug else "INFO"#line:45
        logger .add (sys .stdout ,level =O00OO00OOO000OOO0 )#line:46
        logger .add (OOO00OO00OOOO0O0O ,rotation =logRotationTime ,level =O00OO00OOO000OOO0 )#line:47
    def debug (OOOOO0OOOO0OOOO0O ,O0OOOOOO00000OOO0 ,O0O0OOOO0000O000O ,logFilterKey =""):#line:49
        ""#line:56
        OO000O00OOOOO000O =OOOOO0OOOO0OOOO0O .priGetLogFilterVo (logFilterKey )#line:57
        if OO000O00OOOOO000O is not None and OO000O00OOOOO000O .open is False :#line:58
            return #line:59
        LOG .logger .debug (TEMPLATE_FILE_LOG .format (O0OOOOOO00000OOO0 ,O0O0OOOO0000O000O ))#line:60
    def info (OOOOOO00OO0O00O0O ,OOO0OOOOO0000OOOO ,OOO00OO00O0OO0000 ,logFilterKey =""):#line:62
        ""#line:69
        OOOO0O0O00O0O00O0 =OOOOOO00OO0O00O0O .priGetLogFilterVo (logFilterKey )#line:70
        if OOOO0O0O00O0O00O0 is not None and OOOO0O0O00O0O00O0 .open is False :#line:71
            return #line:72
        LOG .logger .info (TEMPLATE_FILE_LOG .format (OOO0OOOOO0000OOOO ,OOO00OO00O0OO0000 ))#line:73
    def warn (OO000OO0O0O0O000O ,O0O0OO00O0OOOOO0O ,O00O0OOO00O0O0000 ,logFilterKey =""):#line:75
        ""#line:82
        OO0OOO00O0OOOO000 =OO000OO0O0O0O000O .priGetLogFilterVo (logFilterKey )#line:83
        if OO0OOO00O0OOOO000 is not None and OO0OOO00O0OOOO000 .open is False :#line:84
            return #line:85
        LOG .logger .warning (TEMPLATE_FILE_LOG .format (O0O0OO00O0OOOOO0O ,O00O0OOO00O0O0000 ))#line:86
    def error (OO00OO00O00O000OO ,OO00OOOO0000OO0OO ,OOOOO0OO00OO0OO00 ,logFilterKey =""):#line:88
        ""#line:95
        O000000OO00O0000O =OO00OO00O00O000OO .priGetLogFilterVo (logFilterKey )#line:96
        if O000000OO00O0000O is not None and O000000OO00O0000O .open is False :#line:97
            return #line:98
        LOG .logger .error (TEMPLATE_FILE_LOG .format (OO00OOOO0000OO0OO ,OOOOO0OO00OO0OO00 ))#line:99
    def priInitLogFilterKeyVoList (O0O00O0O0O000OOOO ,O0O00O00OOO00O0O0 ):#line:101
        O0O00O0O0O000OOOO .logFilterVoList =[]#line:102
        for OO0OOO0OOOOOO0000 in open (O0O00O00OOO00O0O0 +"resources/logFilter.txt",encoding ="utf-8"):#line:104
            OO00000OOO00O00OO =OO0OOO0OOOOOO0000 .replace ("\n","").split (",")#line:105
            if len (OO00000OOO00O00OO )==3 :#line:106
                O0OOOOOO0O0O0O000 =OO00000OOO00O00OO [0 ]#line:107
                O0OO0O0OO000OOO00 =False if OO00000OOO00O00OO [1 ]=="-"else True #line:108
                OOO00O000OOO00OO0 =True if OO00000OOO00O00OO [2 ]=="A"else False #line:109
                O0O00O0O0O000OOOO .logFilterVoList .append (LogFilterVo (O0OOOOOO0O0O0O000 ,O0OO0O0OO000OOO00 ,OOO00O000OOO00OO0 ))#line:110
        return 1 #line:112
    def priGetLogFilterVo (O0O000OO0O00OO000 ,OO0O00OOOOO0O00OO ):#line:114
        for O0OOO0OOOO0OO00OO ,O00O0O0OOO0O0O0O0 in enumerate (O0O000OO0O00OO000 .logFilterVoList ):#line:115
            if O00O0O0OOO0O0O0O0 .logFilterKey ==OO0O00OOOOO0O00OO :#line:116
                return O00O0O0OOO0O0O0O0 #line:117
        return None #line:118
class LogFilterVo :#line:121
    ""#line:122
    def __init__ (O000O00OOO0000OO0 ,O000000OOOO0OOOO0 ,bOpen =False ,full =True ):#line:124
        ""#line:130
        O000O00OOO0000OO0 .logFilterKey =O000000OOOO0OOOO0 #line:131
        O000O00OOO0000OO0 .open =bOpen #line:132
        O000O00OOO0000OO0 .full =full #line:133
LOG =LogUtilsEx ()#line:136
"""日志对象"""#line:137
if __name__ =="__main__":#line:141
    LOG .init ("../../../appqa/",True )#line:142
    LOG .debug ("WpRun","日志测试1...","调度器-L1-mesInit")#line:143
    LOG .info ("WpRun","日志测试2...","调度器-L1-mesInit")#line:144
    LOG .warn ("WpRun","日志测试3...","调度器-L1-mesInit")#line:145
    LOG .error ("WpRun","日志测试4...","调度器-L1-mesInit")#line:146
