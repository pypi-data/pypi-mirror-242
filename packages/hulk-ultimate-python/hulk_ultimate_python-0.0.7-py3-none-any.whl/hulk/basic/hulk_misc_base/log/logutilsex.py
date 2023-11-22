from loguru import logger #line:1
import os #line:2
import sys #line:3
sys .path .append (os .getcwd ())#line:5
TEMPLATE_FILE_LOG ="[{0}]{1}"#line:7
"""日志模板"""#line:8
class LogUtilsEx :#line:11
    ""#line:12
    def __init__ (OO00O00O0O0O00O0O ):#line:14
        ""#line:15
        OO00O00O0O0O00O0O .logFilterVoList =[]#line:17
        OO00O00O0O0O00O0O .logger =logger #line:20
    def init (O00OO0O0O0OO0OOOO ,dirPathRelativeConf ="",bDebug =False ,fileNameLog ="app.log",logRotationTime ="02:00"):#line:23
        ""#line:31
        O000000000OOOOOO0 =dirPathRelativeConf +"resources/logs"#line:33
        if not os .path .exists (O000000000OOOOOO0 ):#line:34
            os .makedirs (O000000000OOOOOO0 )#line:35
        O00OO0O000O0OO0O0 =os .path .join (O000000000OOOOOO0 ,fileNameLog )#line:36
        O00OO0O0O0OO0OOOO .priInitLogFilterKeyVoList (dirPathRelativeConf )#line:39
        logger .remove ()#line:42
        O0O0000OO0O0000O0 ="DEBUG"if bDebug else "INFO"#line:45
        logger .add (sys .stdout ,level =O0O0000OO0O0000O0 )#line:46
        logger .add (O00OO0O000O0OO0O0 ,rotation =logRotationTime ,level =O0O0000OO0O0000O0 )#line:47
    def debug (OO000O00000O000O0 ,OO000O00O00OOOO00 ,O0O000O00OO0OOOO0 ,logFilterKey =""):#line:49
        ""#line:56
        O0OO0O0OO0O00OOO0 =OO000O00000O000O0 .priGetLogFilterVo (logFilterKey )#line:57
        if O0OO0O0OO0O00OOO0 is not None and O0OO0O0OO0O00OOO0 .open is False :#line:58
            return #line:59
        LOG .logger .debug (TEMPLATE_FILE_LOG .format (OO000O00O00OOOO00 ,O0O000O00OO0OOOO0 ))#line:60
    def info (O00OO00O0O0OO0000 ,O0O0OO00O0O0O00OO ,O0O0OO000O0OOOO00 ,logFilterKey =""):#line:62
        ""#line:69
        OOOO0000OO0O00O0O =O00OO00O0O0OO0000 .priGetLogFilterVo (logFilterKey )#line:70
        if OOOO0000OO0O00O0O is not None and OOOO0000OO0O00O0O .open is False :#line:71
            return #line:72
        LOG .logger .info (TEMPLATE_FILE_LOG .format (O0O0OO00O0O0O00OO ,O0O0OO000O0OOOO00 ))#line:73
    def warn (OO00OO00000OO0OO0 ,O0O00OO0OO0O000O0 ,OO0OO0O0000O0OOOO ,logFilterKey =""):#line:75
        ""#line:82
        OO000O0O00O000O0O =OO00OO00000OO0OO0 .priGetLogFilterVo (logFilterKey )#line:83
        if OO000O0O00O000O0O is not None and OO000O0O00O000O0O .open is False :#line:84
            return #line:85
        LOG .logger .warning (TEMPLATE_FILE_LOG .format (O0O00OO0OO0O000O0 ,OO0OO0O0000O0OOOO ))#line:86
    def error (O0000O00OO000000O ,OOO0O0OO0OOO000O0 ,OO00O0OOOOO00000O ,logFilterKey =""):#line:88
        ""#line:95
        OO0OO0OOOOO000OOO =O0000O00OO000000O .priGetLogFilterVo (logFilterKey )#line:96
        if OO0OO0OOOOO000OOO is not None and OO0OO0OOOOO000OOO .open is False :#line:97
            return #line:98
        LOG .logger .error (TEMPLATE_FILE_LOG .format (OOO0O0OO0OOO000O0 ,OO00O0OOOOO00000O ))#line:99
    def priInitLogFilterKeyVoList (OOO0O000OO0OO00O0 ,O00O0000OO0OO0O00 ):#line:101
        OOO0O000OO0OO00O0 .logFilterVoList =[]#line:102
        for OO0O00O0O0OO0OO00 in open (O00O0000OO0OO0O00 +"resources/logFilter.txt",encoding ="utf-8"):#line:104
            O00OO00O0OO000O0O =OO0O00O0O0OO0OO00 .replace ("\n","").split (",")#line:105
            if len (O00OO00O0OO000O0O )==3 :#line:106
                O0O00O0OOO00OO00O =O00OO00O0OO000O0O [0 ]#line:107
                O0OOO00000O0O000O =False if O00OO00O0OO000O0O [1 ]=="-"else True #line:108
                O0O0OOO0000OO000O =True if O00OO00O0OO000O0O [2 ]=="A"else False #line:109
                OOO0O000OO0OO00O0 .logFilterVoList .append (LogFilterVo (O0O00O0OOO00OO00O ,O0OOO00000O0O000O ,O0O0OOO0000OO000O ))#line:110
        return 1 #line:112
    def priGetLogFilterVo (OO0000OOO000O0OO0 ,O0OO0O0000000O00O ):#line:114
        for O00000OO0OOO00O00 ,O00OO0OO0000OOOO0 in enumerate (OO0000OOO000O0OO0 .logFilterVoList ):#line:115
            if O00OO0OO0000OOOO0 .logFilterKey ==O0OO0O0000000O00O :#line:116
                return O00OO0OO0000OOOO0 #line:117
        return None #line:118
class LogFilterVo :#line:121
    ""#line:122
    def __init__ (OOO0000OO00OO0OOO ,O0O0O0OOO00O00OO0 ,bOpen =False ,full =True ):#line:124
        ""#line:130
        OOO0000OO00OO0OOO .logFilterKey =O0O0O0OOO00O00OO0 #line:131
        OOO0000OO00OO0OOO .open =bOpen #line:132
        OOO0000OO00OO0OOO .full =full #line:133
LOG =LogUtilsEx ()#line:136
"""日志对象"""#line:137
if __name__ =="__main__":#line:141
    LOG .init ("../../../appqa/",True )#line:142
    LOG .debug ("WpRun","日志测试1...","调度器-L1-mesInit")#line:143
    LOG .info ("WpRun","日志测试2...","调度器-L1-mesInit")#line:144
    LOG .warn ("WpRun","日志测试3...","调度器-L1-mesInit")#line:145
    LOG .error ("WpRun","日志测试4...","调度器-L1-mesInit")#line:146
