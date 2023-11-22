from loguru import logger #line:1
import os #line:2
import sys #line:3
sys .path .append (os .getcwd ())#line:5
TEMPLATE_FILE_LOG ="[{0}]{1}"#line:7
"""日志模板"""#line:8
class LogUtilsEx :#line:11
    ""#line:12
    def __init__ (OO0O0OOOO0O000O00 ):#line:14
        ""#line:15
        OO0O0OOOO0O000O00 .logFilterVoList =[]#line:17
        OO0O0OOOO0O000O00 .logger =logger #line:20
    def init (OOO00000000O00O0O ,dirPathRelativeConf ="",bDebug =False ,fileNameLog ="app.log",logRotationTime ="02:00"):#line:23
        ""#line:31
        OOOO00O0O00OOOO0O =dirPathRelativeConf +"resources/logs"#line:33
        if not os .path .exists (OOOO00O0O00OOOO0O ):#line:34
            os .makedirs (OOOO00O0O00OOOO0O )#line:35
        O0OO0O0O0000O0O00 =os .path .join (OOOO00O0O00OOOO0O ,fileNameLog )#line:36
        OOO00000000O00O0O .priInitLogFilterKeyVoList (dirPathRelativeConf )#line:39
        logger .remove ()#line:42
        OO0O00OO0O00OO0OO ="DEBUG"if bDebug else "INFO"#line:45
        logger .add (sys .stdout ,level =OO0O00OO0O00OO0OO )#line:46
        logger .add (O0OO0O0O0000O0O00 ,rotation =logRotationTime ,level =OO0O00OO0O00OO0OO )#line:47
    def debug (O0O0O0000O00O000O ,OO00OOO0O0000OO0O ,O00OO0000O000O0O0 ,logFilterKey =""):#line:49
        ""#line:56
        OO0O000O0O0O0O0O0 =O0O0O0000O00O000O .priGetLogFilterVo (logFilterKey )#line:57
        if OO0O000O0O0O0O0O0 is not None and OO0O000O0O0O0O0O0 .open is False :#line:58
            return #line:59
        LOG .logger .debug (TEMPLATE_FILE_LOG .format (OO00OOO0O0000OO0O ,O00OO0000O000O0O0 ))#line:60
    def info (OO00OOO0O000O00O0 ,O0O00O0O0O0000000 ,OOO0OOO00OO00O0OO ,logFilterKey =""):#line:62
        ""#line:69
        OOOOO00O0O00O00O0 =OO00OOO0O000O00O0 .priGetLogFilterVo (logFilterKey )#line:70
        if OOOOO00O0O00O00O0 is not None and OOOOO00O0O00O00O0 .open is False :#line:71
            return #line:72
        LOG .logger .info (TEMPLATE_FILE_LOG .format (O0O00O0O0O0000000 ,OOO0OOO00OO00O0OO ))#line:73
    def warn (O00O00O0OO0OOOO00 ,OO0OOO0OOO00O000O ,O0OO00O00O0OOO0OO ,logFilterKey =""):#line:75
        ""#line:82
        O000O0O0O0000O00O =O00O00O0OO0OOOO00 .priGetLogFilterVo (logFilterKey )#line:83
        if O000O0O0O0000O00O is not None and O000O0O0O0000O00O .open is False :#line:84
            return #line:85
        LOG .logger .warning (TEMPLATE_FILE_LOG .format (OO0OOO0OOO00O000O ,O0OO00O00O0OOO0OO ))#line:86
    def error (O00OO0O000OOO0000 ,O000OOO000OOOOOOO ,OOO00OO0000O0000O ,logFilterKey =""):#line:88
        ""#line:95
        O0O0OOOO0OO0OO000 =O00OO0O000OOO0000 .priGetLogFilterVo (logFilterKey )#line:96
        if O0O0OOOO0OO0OO000 is not None and O0O0OOOO0OO0OO000 .open is False :#line:97
            return #line:98
        LOG .logger .error (TEMPLATE_FILE_LOG .format (O000OOO000OOOOOOO ,OOO00OO0000O0000O ))#line:99
    def priInitLogFilterKeyVoList (OOOOO00O0000O0000 ,O000000O0000O00OO ):#line:101
        OOOOO00O0000O0000 .logFilterVoList =[]#line:102
        for O0OO00OOO00OO0000 in open (O000000O0000O00OO +"resources/logFilter.txt",encoding ="utf-8"):#line:104
            OOO000OOO0O0000O0 =O0OO00OOO00OO0000 .replace ("\n","").split (",")#line:105
            if len (OOO000OOO0O0000O0 )==3 :#line:106
                O00OOOOOOOOO0OOOO =OOO000OOO0O0000O0 [0 ]#line:107
                OOO00O000O000O00O =False if OOO000OOO0O0000O0 [1 ]=="-"else True #line:108
                O00O0O0O000O00O0O =True if OOO000OOO0O0000O0 [2 ]=="A"else False #line:109
                OOOOO00O0000O0000 .logFilterVoList .append (LogFilterVo (O00OOOOOOOOO0OOOO ,OOO00O000O000O00O ,O00O0O0O000O00O0O ))#line:110
        return 1 #line:112
    def priGetLogFilterVo (OO00OO00O0O00O00O ,O000000OOOO000000 ):#line:114
        for O000OO0OOO0OOO0OO ,OO0O00OO000OOOOO0 in enumerate (OO00OO00O0O00O00O .logFilterVoList ):#line:115
            if OO0O00OO000OOOOO0 .logFilterKey ==O000000OOOO000000 :#line:116
                return OO0O00OO000OOOOO0 #line:117
        return None #line:118
class LogFilterVo :#line:121
    ""#line:122
    def __init__ (O0O0O0O00O0O0OO00 ,O0OO0000O0OO000O0 ,bOpen =False ,full =True ):#line:124
        ""#line:130
        O0O0O0O00O0O0OO00 .logFilterKey =O0OO0000O0OO000O0 #line:131
        O0O0O0O00O0O0OO00 .open =bOpen #line:132
        O0O0O0O00O0O0OO00 .full =full #line:133
LOG =LogUtilsEx ()#line:136
"""日志对象"""#line:137
if __name__ =="__main__":#line:141
    LOG .init ("../../../appqa/",True )#line:142
    LOG .debug ("WpRun","日志测试1...","调度器-L1-mesInit")#line:143
    LOG .info ("WpRun","日志测试2...","调度器-L1-mesInit")#line:144
    LOG .warn ("WpRun","日志测试3...","调度器-L1-mesInit")#line:145
    LOG .error ("WpRun","日志测试4...","调度器-L1-mesInit")#line:146
