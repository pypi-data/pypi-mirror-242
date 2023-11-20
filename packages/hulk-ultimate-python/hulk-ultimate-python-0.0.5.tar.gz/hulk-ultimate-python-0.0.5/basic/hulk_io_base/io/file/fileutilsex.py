import os #line:1
import shutil #line:2
import sys #line:3
import datetime #line:4
sys .path .append (os .getcwd ())#line:6
class FileUtilsEx :#line:9
    ""#line:10
    def __init__ (O0OOO0OOOO0OOO000 ):#line:12
        ""#line:13
    @staticmethod #line:15
    def delFile (O00OOO0OOO00000OO ):#line:16
        ""#line:21
        FileUtilsEx .priDelFile (O00OOO0OOO00000OO )#line:23
    @staticmethod #line:25
    def delFileAndCreateFileEmpty (O00O0O00OO0O00O00 ):#line:26
        ""#line:31
        FileUtilsEx .priDelFile (O00O0O00OO0O00O00 )#line:33
        FileUtilsEx .priCreateFileEmpty (O00O0O00OO0O00O00 )#line:35
    @staticmethod #line:37
    def writeAllText (OOO00O0OO000O00OO ,OO00OOOOO0000OO0O ):#line:38
        ""#line:44
        FileUtilsEx .delFileAndCreateFileEmpty (OOO00O0OO000O00OO )#line:45
        with open (OOO00O0OO000O00OO ,"w",encoding ="utf-8")as O00OO0OO0O0000OO0 :#line:46
            O00OO0OO0O0000OO0 .write (OO00OOOOO0000OO0O )#line:47
    @staticmethod #line:49
    def readAllText (O000O0OOO0O000OOO ):#line:50
        ""#line:55
        with open (O000O0OOO0O000OOO ,"r",encoding ="utf-8")as O000OO000000OO0OO :#line:56
            OO00OO0O0OOOO0O0O =O000OO000000OO0OO .read ()#line:57
        return OO00OO0O0OOOO0O0O #line:58
    @staticmethod #line:60
    def readAllLines (OO0OOOO00O0O000O0 ):#line:61
        ""#line:66
        OOO0OO0O00O000O0O =FileUtilsEx .readAllText (OO0OOOO00O0O000O0 )#line:67
        return OOO0OO0O00O000O0O .split ("\n")#line:68
    @staticmethod #line:70
    def appendFile (O0OOOO000OO0OOO00 ,O0OO0O0O00O00O00O ):#line:71
        ""#line:77
        FileUtilsEx .priCreateFileEmpty (O0OOOO000OO0OOO00 )#line:78
        with open (O0OOOO000OO0OOO00 ,"a",encoding ="utf-8")as O0O0000000O0OO0OO :#line:79
            O0O0000000O0OO0OO .write (O0OO0O0O00O00O00O )#line:80
    @staticmethod #line:82
    def appendFileWithDateTime (O0OOOO0OO00000OO0 ,O0O00O0OOOO0O00O0 ):#line:83
        ""#line:89
        O000OO000O00O0OOO =FileUtilsEx .priGenFilePathByDateTime (O0OOOO0OO00000OO0 )#line:90
        FileUtilsEx .appendFile (O000OO000O00O0OOO ,O0O00O0OOOO0O00O0 )#line:91
    @staticmethod #line:93
    def copyFile (OO0O0O0O0O0OO0OO0 ,O0O00OO0000000O0O ):#line:94
        ""#line:100
        FileUtilsEx .priCreateFileEmpty (O0O00OO0000000O0O )#line:103
        shutil .copy2 (OO0O0O0O0O0OO0OO0 ,O0O00OO0000000O0O )#line:105
    @staticmethod #line:107
    def iterAllFiles (OO0000OO0O0OO0O0O ,O00OOOO00O0O0OOO0 ):#line:108
        ""#line:114
        for O00OO000OOO0OOOOO ,OOO0O00OOO0O0O00O ,OOOOO00O0OO0000OO in os .walk (OO0000OO0O0OO0O0O ):#line:115
            for O0O00O0OOOOOOO000 in OOOOO00O0OO0000OO :#line:116
                if O0O00O0OOOOOOO000 .endswith (O00OOOO00O0O0OOO0 ):#line:117
                    OOOOO0OO0OO00000O =os .path .join (O00OO000OOO0OOOOO ,O0O00O0OOOOOOO000 )#line:118
                    yield OOOOO0OO0OO00000O #line:119
    @staticmethod #line:121
    def priGetDirPath (OO000O0O00O000OOO ):#line:122
        ""#line:127
        return os .path .dirname (OO000O0O00O000OOO )#line:128
    @staticmethod #line:130
    def priCreateDirEmpty (O0O0O0O000O00OOOO ):#line:131
        ""#line:136
        if not os .path .exists (O0O0O0O000O00OOOO ):#line:137
            os .makedirs (O0O0O0O000O00OOOO ,exist_ok =True )#line:138
    @staticmethod #line:140
    def priCreateFileEmpty (OO0000O0OO0000O0O ):#line:141
        ""#line:146
        O00OO0OO00OOOOOOO =FileUtilsEx .priGetDirPath (OO0000O0OO0000O0O )#line:148
        FileUtilsEx .priCreateDirEmpty (O00OO0OO00OOOOOOO )#line:150
        if not os .path .exists (OO0000O0OO0000O0O ):#line:152
            with open (OO0000O0OO0000O0O ,"w",encoding ="utf-8"):#line:153
                pass #line:154
    @staticmethod #line:156
    def priDelFile (OOOO00O000O000O0O ):#line:157
        ""#line:162
        if os .path .exists (OOOO00O000O000O0O ):#line:163
            os .remove (OOOO00O000O000O0O )#line:164
    @staticmethod #line:166
    def priGenFilePathByDateTime (O0O0O0O00O00O0O0O ):#line:167
        ""#line:173
        O0000OO0O00O0000O =os .path .splitext (O0O0O0O00O00O0O0O )#line:174
        O0O0OOO0O00OO0OOO =O0000OO0O00O0000O [0 ]#line:175
        O0OOO00O00OOOOO0O =O0000OO0O00O0000O [-1 ]#line:176
        OO0O0O0O0O0O0O000 =datetime .date .today ().strftime ("%Y-%m-%d")#line:177
        return O0O0OOO0O00OO0OOO +"_"+OO0O0O0O0O0O0O000 +O0OOO00O00OOOOO0O #line:178
if __name__ =='__main__':#line:181
    print (1 )#line:189
