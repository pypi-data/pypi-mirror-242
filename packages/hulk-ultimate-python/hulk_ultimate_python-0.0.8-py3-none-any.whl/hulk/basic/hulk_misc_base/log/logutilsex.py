from loguru import logger #line:1
import os #line:2
import sys #line:3
sys .path .append (os .getcwd ())#line:5
TEMPLATE_FILE_LOG ="[{0}]{1}"#line:7
"""日志模板"""#line:8
class LogUtilsEx :#line:11
    ""#line:12
    def __init__ (O0O0O0O0OO0OOO00O ):#line:14
        ""#line:15
        O0O0O0O0OO0OOO00O .logFilterVoList =[]#line:17
        O0O0O0O0OO0OOO00O .logger =logger #line:20
    def init (OO00000O0000OOOOO ,dirPathRelativeConf ="",bDebug =False ,fileNameLog ="app.log",logRotationTime ="02:00"):#line:23
        ""#line:31
        OO0000OO0O0OO0OOO =dirPathRelativeConf +"resources/logs"#line:33
        if not os .path .exists (OO0000OO0O0OO0OOO ):#line:34
            os .makedirs (OO0000OO0O0OO0OOO )#line:35
        OO0O000000OOOO000 =os .path .join (OO0000OO0O0OO0OOO ,fileNameLog )#line:36
        OO00000O0000OOOOO .priInitLogFilterKeyVoList (dirPathRelativeConf )#line:39
        logger .remove ()#line:42
        O0000OO0000O0OO0O ="DEBUG"if bDebug else "INFO"#line:45
        logger .add (sys .stdout ,level =O0000OO0000O0OO0O )#line:46
        logger .add (OO0O000000OOOO000 ,rotation =logRotationTime ,level =O0000OO0000O0OO0O )#line:47
    def debug (OO0OOOOO00000O00O ,OO0OO000O0OOO00OO ,O0OOOOOO0O0O00OOO ,logFilterKey =""):#line:49
        ""#line:56
        O000OOOO000O0OO00 =OO0OOOOO00000O00O .priGetLogFilterVo (logFilterKey )#line:57
        if O000OOOO000O0OO00 is not None and O000OOOO000O0OO00 .open is False :#line:58
            return #line:59
        LOG .logger .debug (TEMPLATE_FILE_LOG .format (OO0OO000O0OOO00OO ,O0OOOOOO0O0O00OOO ))#line:60
    def info (O00000O000O00O0O0 ,O0O0OOOOO0OO0OO0O ,O0OOO00O0OO0O00O0 ,logFilterKey =""):#line:62
        ""#line:69
        O00OO0000O0O00O00 =O00000O000O00O0O0 .priGetLogFilterVo (logFilterKey )#line:70
        if O00OO0000O0O00O00 is not None and O00OO0000O0O00O00 .open is False :#line:71
            return #line:72
        LOG .logger .info (TEMPLATE_FILE_LOG .format (O0O0OOOOO0OO0OO0O ,O0OOO00O0OO0O00O0 ))#line:73
    def warn (OO0OO0OO0O0O00000 ,OO0OOOOOOOO0O0OO0 ,O0OO000OOO00O00O0 ,logFilterKey =""):#line:75
        ""#line:82
        OOO00OO0OO00O00O0 =OO0OO0OO0O0O00000 .priGetLogFilterVo (logFilterKey )#line:83
        if OOO00OO0OO00O00O0 is not None and OOO00OO0OO00O00O0 .open is False :#line:84
            return #line:85
        LOG .logger .warning (TEMPLATE_FILE_LOG .format (OO0OOOOOOOO0O0OO0 ,O0OO000OOO00O00O0 ))#line:86
    def error (OOOOO0OOOO0OOO00O ,O0O0OOO0OOO00OOO0 ,OO0OOOO00000O00OO ,logFilterKey =""):#line:88
        ""#line:95
        O0O000O0OOOO00OO0 =OOOOO0OOOO0OOO00O .priGetLogFilterVo (logFilterKey )#line:96
        if O0O000O0OOOO00OO0 is not None and O0O000O0OOOO00OO0 .open is False :#line:97
            return #line:98
        LOG .logger .error (TEMPLATE_FILE_LOG .format (O0O0OOO0OOO00OOO0 ,OO0OOOO00000O00OO ))#line:99
    def priInitLogFilterKeyVoList (O0O00O00000000O0O ,O00000O0OO00OOO0O ):#line:101
        O0O00O00000000O0O .logFilterVoList =[]#line:102
        for OOO0OO000O0O0OO00 in open (O00000O0OO00OOO0O +"resources/logFilter.txt",encoding ="utf-8"):#line:104
            O00OOO0OO00OO0OO0 =OOO0OO000O0O0OO00 .replace ("\n","").split (",")#line:105
            if len (O00OOO0OO00OO0OO0 )==3 :#line:106
                O00OO0OOO0OOO0000 =O00OOO0OO00OO0OO0 [0 ]#line:107
                O0O0000OO00OO00OO =False if O00OOO0OO00OO0OO0 [1 ]=="-"else True #line:108
                O00O00000000O0OOO =True if O00OOO0OO00OO0OO0 [2 ]=="A"else False #line:109
                O0O00O00000000O0O .logFilterVoList .append (LogFilterVo (O00OO0OOO0OOO0000 ,O0O0000OO00OO00OO ,O00O00000000O0OOO ))#line:110
        return 1 #line:112
    def priGetLogFilterVo (O00OOO00O0000000O ,O00OO0000OOOOO0O0 ):#line:114
        for O0O0OO00OOOOO000O ,OOO0O000OOOOOO000 in enumerate (O00OOO00O0000000O .logFilterVoList ):#line:115
            if OOO0O000OOOOOO000 .logFilterKey ==O00OO0000OOOOO0O0 :#line:116
                return OOO0O000OOOOOO000 #line:117
        return None #line:118
class LogFilterVo :#line:121
    ""#line:122
    def __init__ (O00O0OO0OOOO0O000 ,O0OO00OOOO0OO0OO0 ,bOpen =False ,full =True ):#line:124
        ""#line:130
        O00O0OO0OOOO0O000 .logFilterKey =O0OO00OOOO0OO0OO0 #line:131
        O00O0OO0OOOO0O000 .open =bOpen #line:132
        O00O0OO0OOOO0O000 .full =full #line:133
LOG =LogUtilsEx ()#line:136
"""日志对象"""#line:137
if __name__ =="__main__":#line:141
    LOG .init ("../../../appqa/",True )#line:142
    LOG .debug ("WpRun","日志测试1...","调度器-L1-mesInit")#line:143
    LOG .info ("WpRun","日志测试2...","调度器-L1-mesInit")#line:144
    LOG .warn ("WpRun","日志测试3...","调度器-L1-mesInit")#line:145
    LOG .error ("WpRun","日志测试4...","调度器-L1-mesInit")#line:146
