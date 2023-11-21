import os #line:1
import shutil #line:2
import sys #line:3
import datetime #line:4
sys .path .append (os .getcwd ())#line:6
class FileUtilsEx :#line:9
    ""#line:10
    def __init__ (O0OOOO0OO00000OOO ):#line:12
        ""#line:13
    @staticmethod #line:15
    def delFile (O00O0000O0OOO0O0O ):#line:16
        ""#line:21
        FileUtilsEx .priDelFile (O00O0000O0OOO0O0O )#line:23
    @staticmethod #line:25
    def delFileAndCreateFileEmpty (O00O0OOO000OOO000 ):#line:26
        ""#line:31
        FileUtilsEx .priDelFile (O00O0OOO000OOO000 )#line:33
        FileUtilsEx .priCreateFileEmpty (O00O0OOO000OOO000 )#line:35
    @staticmethod #line:37
    def writeAllText (O0OOOOOOOOOOOO0OO ,O00000O00OOOOOO00 ):#line:38
        ""#line:44
        FileUtilsEx .delFileAndCreateFileEmpty (O0OOOOOOOOOOOO0OO )#line:45
        with open (O0OOOOOOOOOOOO0OO ,"w",encoding ="utf-8")as OO00000O000OO0OOO :#line:46
            OO00000O000OO0OOO .write (O00000O00OOOOOO00 )#line:47
    @staticmethod #line:49
    def readAllText (OOO000O0OO000OOOO ):#line:50
        ""#line:55
        with open (OOO000O0OO000OOOO ,"r",encoding ="utf-8")as O000OOO000OOOOOO0 :#line:56
            OO0O0O0O00OO00OO0 =O000OOO000OOOOOO0 .read ()#line:57
        return OO0O0O0O00OO00OO0 #line:58
    @staticmethod #line:60
    def readAllLines (OO00O000OO0000OOO ):#line:61
        ""#line:66
        OO00O00OO00OO0OOO =FileUtilsEx .readAllText (OO00O000OO0000OOO )#line:67
        return OO00O00OO00OO0OOO .split ("\n")#line:68
    @staticmethod #line:70
    def appendFile (OOOO00O0O00OOO00O ,O0O00OO0000OOOO0O ):#line:71
        ""#line:77
        FileUtilsEx .priCreateFileEmpty (OOOO00O0O00OOO00O )#line:78
        with open (OOOO00O0O00OOO00O ,"a",encoding ="utf-8")as OO0O0O00O0O0000OO :#line:79
            OO0O0O00O0O0000OO .write (O0O00OO0000OOOO0O )#line:80
    @staticmethod #line:82
    def appendFileWithDateTime (OO0OO00OOO0OO0000 ,O00O000000OOO0OOO ):#line:83
        ""#line:89
        OO00O000O0OOOO0O0 =FileUtilsEx .priGenFilePathByDateTime (OO0OO00OOO0OO0000 )#line:90
        FileUtilsEx .appendFile (OO00O000O0OOOO0O0 ,O00O000000OOO0OOO )#line:91
    @staticmethod #line:93
    def copyFile (O0000O0OOOO000O0O ,O0O00O0OO0O0O0O0O ):#line:94
        ""#line:100
        FileUtilsEx .priCreateFileEmpty (O0O00O0OO0O0O0O0O )#line:103
        shutil .copy2 (O0000O0OOOO000O0O ,O0O00O0OO0O0O0O0O )#line:105
    @staticmethod #line:107
    def iterAllFiles (OO00O00000O0000OO ,O000O00O000O0OO00 ):#line:108
        ""#line:114
        for O00O00OO0OOO000OO ,O00O0O000OOO0OOOO ,O0000000O0O000OOO in os .walk (OO00O00000O0000OO ):#line:115
            for OO00O00OO00O0000O in O0000000O0O000OOO :#line:116
                if OO00O00OO00O0000O .endswith (O000O00O000O0OO00 ):#line:117
                    O0OOOO00000O0OOOO =os .path .join (O00O00OO0OOO000OO ,OO00O00OO00O0000O )#line:118
                    yield O0OOOO00000O0OOOO #line:119
    @staticmethod #line:121
    def priGetDirPath (O0O0OOO0OOO00OOO0 ):#line:122
        ""#line:127
        return os .path .dirname (O0O0OOO0OOO00OOO0 )#line:128
    @staticmethod #line:130
    def priCreateDirEmpty (O000O0OOO0OO00O0O ):#line:131
        ""#line:136
        if not os .path .exists (O000O0OOO0OO00O0O ):#line:137
            os .makedirs (O000O0OOO0OO00O0O ,exist_ok =True )#line:138
    @staticmethod #line:140
    def priCreateFileEmpty (OO0OOO00OO0O000OO ):#line:141
        ""#line:146
        OOOO0OOOO0OO00OO0 =FileUtilsEx .priGetDirPath (OO0OOO00OO0O000OO )#line:148
        FileUtilsEx .priCreateDirEmpty (OOOO0OOOO0OO00OO0 )#line:150
        if not os .path .exists (OO0OOO00OO0O000OO ):#line:152
            with open (OO0OOO00OO0O000OO ,"w",encoding ="utf-8"):#line:153
                pass #line:154
    @staticmethod #line:156
    def priDelFile (OO00O0OOO00O00OO0 ):#line:157
        ""#line:162
        if os .path .exists (OO00O0OOO00O00OO0 ):#line:163
            os .remove (OO00O0OOO00O00OO0 )#line:164
    @staticmethod #line:166
    def priGenFilePathByDateTime (O000000OOO0O0O00O ):#line:167
        ""#line:173
        OO0OOOOOOOOO0OO00 =os .path .splitext (O000000OOO0O0O00O )#line:174
        O00OO0O00OO000OO0 =OO0OOOOOOOOO0OO00 [0 ]#line:175
        OO00000O0O0O00O0O =OO0OOOOOOOOO0OO00 [-1 ]#line:176
        O00OO0O00000O0OOO =datetime .date .today ().strftime ("%Y-%m-%d")#line:177
        return O00OO0O00OO000OO0 +"_"+O00OO0O00000O0OOO +OO00000O0O0O00O0O #line:178
if __name__ =='__main__':#line:181
    print (1 )#line:189
