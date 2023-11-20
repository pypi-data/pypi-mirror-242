from loguru import logger #line:1
import os #line:2
import sys #line:3
sys .path .append (os .getcwd ())#line:5
TEMPLATE_FILE_LOG ="[{0}]{1}"#line:7
"""日志模板"""#line:8
class LogUtilsEx :#line:11
    ""#line:12
    def __init__ (OOOOO000OO0OO0OO0 ):#line:14
        ""#line:15
        OOOOO000OO0OO0OO0 .logFilterVoList =[]#line:17
        OOOOO000OO0OO0OO0 .logger =logger #line:20
    def init (OO000O0OO000O0O00 ,dirPathRelativeConf ="",bDebug =False ,fileNameLog ="app.log",logRotationTime ="02:00"):#line:23
        ""#line:31
        OOOOOOOO0O00O0OOO =dirPathRelativeConf +"resources/logs"#line:33
        if not os .path .exists (OOOOOOOO0O00O0OOO ):#line:34
            os .makedirs (OOOOOOOO0O00O0OOO )#line:35
        O0O000OOOO000OOOO =os .path .join (OOOOOOOO0O00O0OOO ,fileNameLog )#line:36
        OO000O0OO000O0O00 .priInitLogFilterKeyVoList (dirPathRelativeConf )#line:39
        logger .remove ()#line:42
        O0OOO0000O000OOOO ="DEBUG"if bDebug else "INFO"#line:45
        logger .add (sys .stdout ,level =O0OOO0000O000OOOO )#line:46
        logger .add (O0O000OOOO000OOOO ,rotation =logRotationTime ,level =O0OOO0000O000OOOO )#line:47
    def debug (O0OO0O000O0OO0OOO ,O00O0OO0OOOOO000O ,OOOOOOO0OO0O0000O ,logFilterKey =""):#line:49
        ""#line:56
        OO0OO0O0O0000OOOO =O0OO0O000O0OO0OOO .priGetLogFilterVo (logFilterKey )#line:57
        if OO0OO0O0O0000OOOO is not None and OO0OO0O0O0000OOOO .open is False :#line:58
            return #line:59
        LOG .logger .debug (TEMPLATE_FILE_LOG .format (O00O0OO0OOOOO000O ,OOOOOOO0OO0O0000O ))#line:60
    def info (OOOO00O000OOO0O00 ,O000O00O0OOOO00OO ,OO0O000O0OO0O00O0 ,logFilterKey =""):#line:62
        ""#line:69
        O00O000000OOO0OOO =OOOO00O000OOO0O00 .priGetLogFilterVo (logFilterKey )#line:70
        if O00O000000OOO0OOO is not None and O00O000000OOO0OOO .open is False :#line:71
            return #line:72
        LOG .logger .info (TEMPLATE_FILE_LOG .format (O000O00O0OOOO00OO ,OO0O000O0OO0O00O0 ))#line:73
    def warn (OOO0000OOO00OO0O0 ,O00O0O0OO000O00OO ,OOOO0O0OOOOO0O000 ,logFilterKey =""):#line:75
        ""#line:82
        OO0OOO0OO0O0O00OO =OOO0000OOO00OO0O0 .priGetLogFilterVo (logFilterKey )#line:83
        if OO0OOO0OO0O0O00OO is not None and OO0OOO0OO0O0O00OO .open is False :#line:84
            return #line:85
        LOG .logger .warning (TEMPLATE_FILE_LOG .format (O00O0O0OO000O00OO ,OOOO0O0OOOOO0O000 ))#line:86
    def error (OO0OOOOO0O00O00O0 ,OO0OOOOO00O0O0O0O ,O0OOOO00000OOOOO0 ,logFilterKey =""):#line:88
        ""#line:95
        O0O0OO0OOOO00O0O0 =OO0OOOOO0O00O00O0 .priGetLogFilterVo (logFilterKey )#line:96
        if O0O0OO0OOOO00O0O0 is not None and O0O0OO0OOOO00O0O0 .open is False :#line:97
            return #line:98
        LOG .logger .error (TEMPLATE_FILE_LOG .format (OO0OOOOO00O0O0O0O ,O0OOOO00000OOOOO0 ))#line:99
    def priInitLogFilterKeyVoList (O0O000OOO00O0O0OO ,OO00OOO0O0O0O0O00 ):#line:101
        O0O000OOO00O0O0OO .logFilterVoList =[]#line:102
        for O0OO0O0O000000O0O in open (OO00OOO0O0O0O0O00 +"resources/logFilter.txt",encoding ="utf-8"):#line:104
            O0000000O0OOO0O00 =O0OO0O0O000000O0O .replace ("\n","").split (",")#line:105
            if len (O0000000O0OOO0O00 )==3 :#line:106
                OOOOOOO0OO000OO00 =O0000000O0OOO0O00 [0 ]#line:107
                OO0O00O0OOOO00000 =False if O0000000O0OOO0O00 [1 ]=="-"else True #line:108
                OO0000OO0000OOO0O =True if O0000000O0OOO0O00 [2 ]=="A"else False #line:109
                O0O000OOO00O0O0OO .logFilterVoList .append (LogFilterVo (OOOOOOO0OO000OO00 ,OO0O00O0OOOO00000 ,OO0000OO0000OOO0O ))#line:110
        return 1 #line:112
    def priGetLogFilterVo (O000O0O0OO00O000O ,O00OO0OO00000OO00 ):#line:114
        for O0OOOO0O0O0OO000O ,OOO0000OO0O000O0O in enumerate (O000O0O0OO00O000O .logFilterVoList ):#line:115
            if OOO0000OO0O000O0O .logFilterKey ==O00OO0OO00000OO00 :#line:116
                return OOO0000OO0O000O0O #line:117
        return None #line:118
class LogFilterVo :#line:121
    ""#line:122
    def __init__ (OOO0O0OOOOO0OO000 ,O00O000O00000OO00 ,bOpen =False ,full =True ):#line:124
        ""#line:130
        OOO0O0OOOOO0OO000 .logFilterKey =O00O000O00000OO00 #line:131
        OOO0O0OOOOO0OO000 .open =bOpen #line:132
        OOO0O0OOOOO0OO000 .full =full #line:133
LOG =LogUtilsEx ()#line:136
"""日志对象"""#line:137
if __name__ =="__main__":#line:141
    LOG .init ("../../../appqa/",True )#line:142
    LOG .debug ("WpRun","日志测试1...","调度器-L1-mesInit")#line:143
    LOG .info ("WpRun","日志测试2...","调度器-L1-mesInit")#line:144
    LOG .warn ("WpRun","日志测试3...","调度器-L1-mesInit")#line:145
    LOG .error ("WpRun","日志测试4...","调度器-L1-mesInit")#line:146
