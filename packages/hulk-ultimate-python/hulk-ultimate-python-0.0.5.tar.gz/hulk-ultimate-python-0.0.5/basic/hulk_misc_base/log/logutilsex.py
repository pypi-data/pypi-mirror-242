from loguru import logger #line:1
import os #line:2
import sys #line:3
sys .path .append (os .getcwd ())#line:5
TEMPLATE_FILE_LOG ="[{0}]{1}"#line:7
"""日志模板"""#line:8
class LogUtilsEx :#line:11
    ""#line:12
    def __init__ (O00OOOOO0OO000O00 ):#line:14
        ""#line:15
        O00OOOOO0OO000O00 .logFilterVoList =[]#line:17
        O00OOOOO0OO000O00 .logger =logger #line:20
    def init (O0OO0O0OOOO0OOO00 ,dirPathRelativeConf ="",bDebug =False ,fileNameLog ="app.log",logRotationTime ="02:00"):#line:23
        ""#line:31
        O000OO0O00OO00O0O =dirPathRelativeConf +"resources/logs"#line:33
        if not os .path .exists (O000OO0O00OO00O0O ):#line:34
            os .makedirs (O000OO0O00OO00O0O )#line:35
        O000O00O000OOO00O =os .path .join (O000OO0O00OO00O0O ,fileNameLog )#line:36
        O0OO0O0OOOO0OOO00 .priInitLogFilterKeyVoList (dirPathRelativeConf )#line:39
        logger .remove ()#line:42
        O0OOOO000000O0OO0 ="DEBUG"if bDebug else "INFO"#line:45
        logger .add (sys .stdout ,level =O0OOOO000000O0OO0 )#line:46
        logger .add (O000O00O000OOO00O ,rotation =logRotationTime ,level =O0OOOO000000O0OO0 )#line:47
    def debug (OOOO0O0OO00O0OOOO ,O00O000OO0OO00OO0 ,OO0OO00O00O000OOO ,logFilterKey =""):#line:49
        ""#line:56
        OO0O00OOO00OO000O =OOOO0O0OO00O0OOOO .priGetLogFilterVo (logFilterKey )#line:57
        if OO0O00OOO00OO000O is not None and OO0O00OOO00OO000O .open is False :#line:58
            return #line:59
        LOG .logger .debug (TEMPLATE_FILE_LOG .format (O00O000OO0OO00OO0 ,OO0OO00O00O000OOO ))#line:60
    def info (OOO0OOO0O000OO00O ,OO000O000O0O0O0O0 ,OOOOO00O0OOOOOO0O ,logFilterKey =""):#line:62
        ""#line:69
        OO0OO00O0OO0OOO00 =OOO0OOO0O000OO00O .priGetLogFilterVo (logFilterKey )#line:70
        if OO0OO00O0OO0OOO00 is not None and OO0OO00O0OO0OOO00 .open is False :#line:71
            return #line:72
        LOG .logger .info (TEMPLATE_FILE_LOG .format (OO000O000O0O0O0O0 ,OOOOO00O0OOOOOO0O ))#line:73
    def warn (O000OOO00O000OO00 ,O0O00OO00O0O0O0O0 ,OOOO0O0O00OO0O0O0 ,logFilterKey =""):#line:75
        ""#line:82
        O0O0OOO0O0OOO0O0O =O000OOO00O000OO00 .priGetLogFilterVo (logFilterKey )#line:83
        if O0O0OOO0O0OOO0O0O is not None and O0O0OOO0O0OOO0O0O .open is False :#line:84
            return #line:85
        LOG .logger .warning (TEMPLATE_FILE_LOG .format (O0O00OO00O0O0O0O0 ,OOOO0O0O00OO0O0O0 ))#line:86
    def error (O000OO000O00O0OOO ,O0OO00OO0O000O0OO ,OO0O000000OOO0OO0 ,logFilterKey =""):#line:88
        ""#line:95
        O0OO0O0OOOO0OO000 =O000OO000O00O0OOO .priGetLogFilterVo (logFilterKey )#line:96
        if O0OO0O0OOOO0OO000 is not None and O0OO0O0OOOO0OO000 .open is False :#line:97
            return #line:98
        LOG .logger .error (TEMPLATE_FILE_LOG .format (O0OO00OO0O000O0OO ,OO0O000000OOO0OO0 ))#line:99
    def priInitLogFilterKeyVoList (OOOOOOOO00OO0OO00 ,OOO0O00O0OO0OO00O ):#line:101
        OOOOOOOO00OO0OO00 .logFilterVoList =[]#line:102
        for O00O00O0O00O00OOO in open (OOO0O00O0OO0OO00O +"resources/logFilter.txt",encoding ="utf-8"):#line:104
            O000OO0000OOOO0OO =O00O00O0O00O00OOO .replace ("\n","").split (",")#line:105
            if len (O000OO0000OOOO0OO )==3 :#line:106
                OOO0O00OO00000000 =O000OO0000OOOO0OO [0 ]#line:107
                OOO00000OOO00O000 =False if O000OO0000OOOO0OO [1 ]=="-"else True #line:108
                O00000O00O00O000O =True if O000OO0000OOOO0OO [2 ]=="A"else False #line:109
                OOOOOOOO00OO0OO00 .logFilterVoList .append (LogFilterVo (OOO0O00OO00000000 ,OOO00000OOO00O000 ,O00000O00O00O000O ))#line:110
        return 1 #line:112
    def priGetLogFilterVo (OOOOO0O0000OO00OO ,OO000O0000OO0OO00 ):#line:114
        for OO000O00OOO0000O0 ,O00O00OOO0000000O in enumerate (OOOOO0O0000OO00OO .logFilterVoList ):#line:115
            if O00O00OOO0000000O .logFilterKey ==OO000O0000OO0OO00 :#line:116
                return O00O00OOO0000000O #line:117
        return None #line:118
class LogFilterVo :#line:121
    ""#line:122
    def __init__ (OOOO0O00O0O00O0OO ,OO000000000O00OO0 ,bOpen =False ,full =True ):#line:124
        ""#line:130
        OOOO0O00O0O00O0OO .logFilterKey =OO000000000O00OO0 #line:131
        OOOO0O00O0O00O0OO .open =bOpen #line:132
        OOOO0O00O0O00O0OO .full =full #line:133
LOG =LogUtilsEx ()#line:136
"""日志对象"""#line:137
if __name__ =="__main__":#line:141
    LOG .init ("../../../appqa/",True )#line:142
    LOG .debug ("WpRun","日志测试1...","调度器-L1-mesInit")#line:143
    LOG .info ("WpRun","日志测试2...","调度器-L1-mesInit")#line:144
    LOG .warn ("WpRun","日志测试3...","调度器-L1-mesInit")#line:145
    LOG .error ("WpRun","日志测试4...","调度器-L1-mesInit")#line:146
