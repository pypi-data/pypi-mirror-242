from loguru import logger #line:1
import os #line:2
import sys #line:3
sys .path .append (os .getcwd ())#line:5
TEMPLATE_FILE_LOG ="[{0}]{1}"#line:7
"""日志模板"""#line:8
class LogUtilsEx :#line:11
    ""#line:12
    def __init__ (O00OOOO00OOO00O0O ):#line:14
        ""#line:15
        O00OOOO00OOO00O0O .logFilterVoList =[]#line:17
        O00OOOO00OOO00O0O .logger =logger #line:20
    def init (O0OOOOOOOO0O0OO0O ,dirPathRelativeConf ="",bDebug =False ,fileNameLog ="app.log",logRotationTime ="02:00"):#line:23
        ""#line:31
        O0O000OO0O000000O =dirPathRelativeConf +"resources/logs"#line:33
        if not os .path .exists (O0O000OO0O000000O ):#line:34
            os .makedirs (O0O000OO0O000000O )#line:35
        OO00O00000OOO000O =os .path .join (O0O000OO0O000000O ,fileNameLog )#line:36
        O0OOOOOOOO0O0OO0O .priInitLogFilterKeyVoList (dirPathRelativeConf )#line:39
        logger .remove ()#line:42
        O00OOOO0000O00OO0 ="DEBUG"if bDebug else "INFO"#line:45
        logger .add (sys .stdout ,level =O00OOOO0000O00OO0 )#line:46
        logger .add (OO00O00000OOO000O ,rotation =logRotationTime ,level =O00OOOO0000O00OO0 )#line:47
    def debug (O0OOO0000O00OOO0O ,O0000OO0000OOOO00 ,O000OOOO0000O0O0O ,logFilterKey =""):#line:49
        ""#line:56
        O0O00O00OOO00O0O0 =O0OOO0000O00OOO0O .priGetLogFilterVo (logFilterKey )#line:57
        if O0O00O00OOO00O0O0 is not None and O0O00O00OOO00O0O0 .open is False :#line:58
            return #line:59
        LOG .logger .debug (TEMPLATE_FILE_LOG .format (O0000OO0000OOOO00 ,O000OOOO0000O0O0O ))#line:60
    def info (OOO0O0000O0O0O0O0 ,O00000OO00O00O000 ,O0OOO000OO00OO000 ,logFilterKey =""):#line:62
        ""#line:69
        O00O0O0O000OOO00O =OOO0O0000O0O0O0O0 .priGetLogFilterVo (logFilterKey )#line:70
        if O00O0O0O000OOO00O is not None and O00O0O0O000OOO00O .open is False :#line:71
            return #line:72
        LOG .logger .info (TEMPLATE_FILE_LOG .format (O00000OO00O00O000 ,O0OOO000OO00OO000 ))#line:73
    def warn (O0O0OO0O0O0O0OO00 ,O0OOO00O0OOOOOO00 ,O00O0OO0OO00O0000 ,logFilterKey =""):#line:75
        ""#line:82
        O000OOO00O00OO000 =O0O0OO0O0O0O0OO00 .priGetLogFilterVo (logFilterKey )#line:83
        if O000OOO00O00OO000 is not None and O000OOO00O00OO000 .open is False :#line:84
            return #line:85
        LOG .logger .warning (TEMPLATE_FILE_LOG .format (O0OOO00O0OOOOOO00 ,O00O0OO0OO00O0000 ))#line:86
    def error (OO0O0O0OOOOOOOOO0 ,O0O000OO0O00O00O0 ,OOO0OOO000O0O0OOO ,logFilterKey =""):#line:88
        ""#line:95
        O0O0OO000O0OOO0OO =OO0O0O0OOOOOOOOO0 .priGetLogFilterVo (logFilterKey )#line:96
        if O0O0OO000O0OOO0OO is not None and O0O0OO000O0OOO0OO .open is False :#line:97
            return #line:98
        LOG .logger .error (TEMPLATE_FILE_LOG .format (O0O000OO0O00O00O0 ,OOO0OOO000O0O0OOO ))#line:99
    def priInitLogFilterKeyVoList (O0O000000O0000OOO ,OO000O00O00O0OO0O ):#line:101
        O0O000000O0000OOO .logFilterVoList =[]#line:102
        for OO00O00OOO000OOOO in open (OO000O00O00O0OO0O +"resources/logFilter.txt",encoding ="utf-8"):#line:104
            OO00O0OOOO00O0OOO =OO00O00OOO000OOOO .replace ("\n","").split (",")#line:105
            if len (OO00O0OOOO00O0OOO )==3 :#line:106
                OOO0OOO0OOO00O000 =OO00O0OOOO00O0OOO [0 ]#line:107
                OOO000000OOOOOOO0 =False if OO00O0OOOO00O0OOO [1 ]=="-"else True #line:108
                OO00OOOO000O0O000 =True if OO00O0OOOO00O0OOO [2 ]=="A"else False #line:109
                O0O000000O0000OOO .logFilterVoList .append (LogFilterVo (OOO0OOO0OOO00O000 ,OOO000000OOOOOOO0 ,OO00OOOO000O0O000 ))#line:110
        return 1 #line:112
    def priGetLogFilterVo (OOOO0O0OOO0O0O00O ,O00000O0O0OOOOO0O ):#line:114
        for OO000O00OOO0OOO0O ,OOO000OO00OOO00O0 in enumerate (OOOO0O0OOO0O0O00O .logFilterVoList ):#line:115
            if OOO000OO00OOO00O0 .logFilterKey ==O00000O0O0OOOOO0O :#line:116
                return OOO000OO00OOO00O0 #line:117
        return None #line:118
class LogFilterVo :#line:121
    ""#line:122
    def __init__ (OO0O0O0O0O0000O0O ,OO0O0OO0OO0O0OO0O ,bOpen =False ,full =True ):#line:124
        ""#line:130
        OO0O0O0O0O0000O0O .logFilterKey =OO0O0OO0OO0O0OO0O #line:131
        OO0O0O0O0O0000O0O .open =bOpen #line:132
        OO0O0O0O0O0000O0O .full =full #line:133
LOG =LogUtilsEx ()#line:136
"""日志对象"""#line:137
if __name__ =="__main__":#line:141
    LOG .init ("../../../appqa/",True )#line:142
    LOG .debug ("WpRun","日志测试1...","调度器-L1-mesInit")#line:143
    LOG .info ("WpRun","日志测试2...","调度器-L1-mesInit")#line:144
    LOG .warn ("WpRun","日志测试3...","调度器-L1-mesInit")#line:145
    LOG .error ("WpRun","日志测试4...","调度器-L1-mesInit")#line:146
