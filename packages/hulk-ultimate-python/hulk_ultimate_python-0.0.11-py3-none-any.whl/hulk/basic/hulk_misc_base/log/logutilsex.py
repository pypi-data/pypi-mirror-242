from loguru import logger #line:1
import os #line:2
import sys #line:3
sys .path .append (os .getcwd ())#line:5
TEMPLATE_FILE_LOG ="[{0}]{1}"#line:7
"""日志模板"""#line:8
class LogUtilsEx :#line:11
    ""#line:12
    def __init__ (OO000OOOOO0OOO0O0 ):#line:14
        ""#line:15
        OO000OOOOO0OOO0O0 .logFilterVoList =[]#line:17
        OO000OOOOO0OOO0O0 .logger =logger #line:20
    def init (O0000O0O0OOO0O000 ,dirPathRelativeConf ="",bDebug =False ,fileNameLog ="app.log",logRotationTime ="02:00"):#line:23
        ""#line:31
        O000OO0O0O0O0OOO0 =dirPathRelativeConf +"resources/logs"#line:33
        if not os .path .exists (O000OO0O0O0O0OOO0 ):#line:34
            os .makedirs (O000OO0O0O0O0OOO0 )#line:35
        OOO00O000O0O0000O =os .path .join (O000OO0O0O0O0OOO0 ,fileNameLog )#line:36
        O0000O0O0OOO0O000 .priInitLogFilterKeyVoList (dirPathRelativeConf )#line:39
        logger .remove ()#line:42
        OO0O0O000OOO0O0O0 ="DEBUG"if bDebug else "INFO"#line:45
        logger .add (sys .stdout ,level =OO0O0O000OOO0O0O0 )#line:46
        logger .add (OOO00O000O0O0000O ,rotation =logRotationTime ,level =OO0O0O000OOO0O0O0 )#line:47
    def debug (O000OO0OO00O0OOO0 ,O0O00O0OO0OOOO0OO ,O0O0O0000OOO000O0 ,logFilterKey =""):#line:49
        ""#line:56
        O0OO0000OO00OO00O =O000OO0OO00O0OOO0 .priGetLogFilterVo (logFilterKey )#line:57
        if O0OO0000OO00OO00O is not None and O0OO0000OO00OO00O .open is False :#line:58
            return #line:59
        LOG .logger .debug (TEMPLATE_FILE_LOG .format (O0O00O0OO0OOOO0OO ,O0O0O0000OOO000O0 ))#line:60
    def info (OO000O00000000O0O ,OOO00O0OOOO00000O ,OOOO0O0OO00OOOO00 ,logFilterKey =""):#line:62
        ""#line:69
        O0OOOO0O000OO0O0O =OO000O00000000O0O .priGetLogFilterVo (logFilterKey )#line:70
        if O0OOOO0O000OO0O0O is not None and O0OOOO0O000OO0O0O .open is False :#line:71
            return #line:72
        LOG .logger .info (TEMPLATE_FILE_LOG .format (OOO00O0OOOO00000O ,OOOO0O0OO00OOOO00 ))#line:73
    def warn (O0OO00O0OOO00O00O ,OOOO000OO00O00O0O ,O00OOOO0OOO00OO00 ,logFilterKey =""):#line:75
        ""#line:82
        O00OOO00O00OOO0OO =O0OO00O0OOO00O00O .priGetLogFilterVo (logFilterKey )#line:83
        if O00OOO00O00OOO0OO is not None and O00OOO00O00OOO0OO .open is False :#line:84
            return #line:85
        LOG .logger .warning (TEMPLATE_FILE_LOG .format (OOOO000OO00O00O0O ,O00OOOO0OOO00OO00 ))#line:86
    def error (OOOOOO0OO000OO0OO ,OOOOO000OO000OOOO ,OOO00O0OOOO00O000 ,logFilterKey =""):#line:88
        ""#line:95
        OO0000O00000OO00O =OOOOOO0OO000OO0OO .priGetLogFilterVo (logFilterKey )#line:96
        if OO0000O00000OO00O is not None and OO0000O00000OO00O .open is False :#line:97
            return #line:98
        LOG .logger .error (TEMPLATE_FILE_LOG .format (OOOOO000OO000OOOO ,OOO00O0OOOO00O000 ))#line:99
    def priInitLogFilterKeyVoList (OOOO0O000OO0OOOO0 ,OO00OOOO00OO00000 ):#line:101
        OOOO0O000OO0OOOO0 .logFilterVoList =[]#line:102
        for O0OOO00O0O0OOO0OO in open (OO00OOOO00OO00000 +"resources/logFilter.txt",encoding ="utf-8"):#line:104
            OO000O00OO0O0OO00 =O0OOO00O0O0OOO0OO .replace ("\n","").split (",")#line:105
            if len (OO000O00OO0O0OO00 )==3 :#line:106
                O0OOO0000O000O0O0 =OO000O00OO0O0OO00 [0 ]#line:107
                OOO000O00OOO00OO0 =False if OO000O00OO0O0OO00 [1 ]=="-"else True #line:108
                OOOO0000O00OOOO0O =True if OO000O00OO0O0OO00 [2 ]=="A"else False #line:109
                OOOO0O000OO0OOOO0 .logFilterVoList .append (LogFilterVo (O0OOO0000O000O0O0 ,OOO000O00OOO00OO0 ,OOOO0000O00OOOO0O ))#line:110
        return 1 #line:112
    def priGetLogFilterVo (O0000OOO0000OO0OO ,O0OOOOO0OO0OOO00O ):#line:114
        for OOOO0O0O0O00OOO0O ,OO00OOO000OOO00OO in enumerate (O0000OOO0000OO0OO .logFilterVoList ):#line:115
            if OO00OOO000OOO00OO .logFilterKey ==O0OOOOO0OO0OOO00O :#line:116
                return OO00OOO000OOO00OO #line:117
        return None #line:118
class LogFilterVo :#line:121
    ""#line:122
    def __init__ (OOOO00O00OOO00OO0 ,OOO00O000O00000OO ,bOpen =False ,full =True ):#line:124
        ""#line:130
        OOOO00O00OOO00OO0 .logFilterKey =OOO00O000O00000OO #line:131
        OOOO00O00OOO00OO0 .open =bOpen #line:132
        OOOO00O00OOO00OO0 .full =full #line:133
LOG =LogUtilsEx ()#line:136
"""日志对象"""#line:137
if __name__ =="__main__":#line:141
    LOG .init ("../../../appqa/",True )#line:142
    LOG .debug ("WpRun","日志测试1...","调度器-L1-mesInit")#line:143
    LOG .info ("WpRun","日志测试2...","调度器-L1-mesInit")#line:144
    LOG .warn ("WpRun","日志测试3...","调度器-L1-mesInit")#line:145
    LOG .error ("WpRun","日志测试4...","调度器-L1-mesInit")#line:146
