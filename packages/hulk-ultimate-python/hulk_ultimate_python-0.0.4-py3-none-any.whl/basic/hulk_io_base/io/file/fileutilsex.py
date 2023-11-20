import os #line:1
import shutil #line:2
import sys #line:3
import datetime #line:4
sys .path .append (os .getcwd ())#line:6
class FileUtilsEx :#line:9
    ""#line:10
    def __init__ (O00O0OO0000OO0OOO ):#line:12
        ""#line:13
    @staticmethod #line:15
    def delFileAndCreateFileEmpty (O0O00000000OOOO0O ):#line:16
        ""#line:21
        FileUtilsEx .priDelFile (O0O00000000OOOO0O )#line:23
        FileUtilsEx .priCreateFileEmpty (O0O00000000OOOO0O )#line:25
    @staticmethod #line:27
    def writeAllText (O0O000OO00000O0OO ,O0O00O0OO0O00O00O ):#line:28
        ""#line:34
        FileUtilsEx .delFileAndCreateFileEmpty (O0O000OO00000O0OO )#line:35
        with open (O0O000OO00000O0OO ,"w",encoding ="utf-8")as O000OOOO0O000O00O :#line:36
            O000OOOO0O000O00O .write (O0O00O0OO0O00O00O )#line:37
    @staticmethod #line:39
    def readAllText (O000OO0OOOOO0000O ):#line:40
        ""#line:45
        with open (O000OO0OOOOO0000O ,"r",encoding ="utf-8")as OO0OOO000O0000O0O :#line:46
            O000000O0000OO00O =OO0OOO000O0000O0O .read ()#line:47
        return O000000O0000OO00O #line:48
    @staticmethod #line:50
    def readAllLines (OO00OOO00OOO000O0 ):#line:51
        ""#line:56
        O00OOOO00OOOOOO00 =FileUtilsEx .readAllText (OO00OOO00OOO000O0 )#line:57
        return O00OOOO00OOOOOO00 .split ("\n")#line:58
    @staticmethod #line:60
    def appendFile (OO0OOO000O00OOO0O ,OO0O0O0O0O0OOO000 ):#line:61
        ""#line:67
        FileUtilsEx .priCreateFileEmpty (OO0OOO000O00OOO0O )#line:68
        with open (OO0OOO000O00OOO0O ,"a",encoding ="utf-8")as OOOO0OO0O0O00000O :#line:69
            OOOO0OO0O0O00000O .write (OO0O0O0O0O0OOO000 )#line:70
    @staticmethod #line:72
    def appendFileWithDateTime (OO000O00O00000O0O ,OOOO0OOO0O0O00OOO ):#line:73
        ""#line:79
        OO0O0OOOOO0OO0OO0 =FileUtilsEx .priGenFilePathByDateTime (OO000O00O00000O0O )#line:80
        FileUtilsEx .appendFile (OO0O0OOOOO0OO0OO0 ,OOOO0OOO0O0O00OOO )#line:81
    @staticmethod #line:83
    def copyFile (O0OOO0000OOO0O0OO ,OO0O0O0OO0O0O0OO0 ):#line:84
        ""#line:90
        FileUtilsEx .priCreateFileEmpty (OO0O0O0OO0O0O0OO0 )#line:93
        shutil .copy2 (O0OOO0000OOO0O0OO ,OO0O0O0OO0O0O0OO0 )#line:95
    @staticmethod #line:97
    def iterAllFiles (OO0O00O00O00O00OO ,OO00OOO0OO0OO0000 ):#line:98
        ""#line:104
        for O0O0OOO0OO00OO0O0 ,OO00OOOO00O00000O ,OOOO00OOO0000OOO0 in os .walk (OO0O00O00O00O00OO ):#line:105
            for O0OO0000OOOO00OO0 in OOOO00OOO0000OOO0 :#line:106
                if O0OO0000OOOO00OO0 .endswith (OO00OOO0OO0OO0000 ):#line:107
                    O00000000O0OOO000 =os .path .join (O0O0OOO0OO00OO0O0 ,O0OO0000OOOO00OO0 )#line:108
                    yield O00000000O0OOO000 #line:109
    @staticmethod #line:111
    def priGetDirPath (OO0O0O0O0O0O0O000 ):#line:112
        ""#line:117
        return os .path .dirname (OO0O0O0O0O0O0O000 )#line:118
    @staticmethod #line:120
    def priCreateDirEmpty (OO0OOO0O0OO0OOOOO ):#line:121
        ""#line:126
        if not os .path .exists (OO0OOO0O0OO0OOOOO ):#line:127
            os .makedirs (OO0OOO0O0OO0OOOOO ,exist_ok =True )#line:128
    @staticmethod #line:130
    def priCreateFileEmpty (OOOO00OO00O0OO000 ):#line:131
        ""#line:136
        OO0000OOOOOO00O0O =FileUtilsEx .priGetDirPath (OOOO00OO00O0OO000 )#line:138
        FileUtilsEx .priCreateDirEmpty (OO0000OOOOOO00O0O )#line:140
        if not os .path .exists (OOOO00OO00O0OO000 ):#line:142
            with open (OOOO00OO00O0OO000 ,"w",encoding ="utf-8"):#line:143
                pass #line:144
    @staticmethod #line:146
    def priDelFile (OOO0OO0OO0OO000O0 ):#line:147
        ""#line:152
        if os .path .exists (OOO0OO0OO0OO000O0 ):#line:153
            os .remove (OOO0OO0OO0OO000O0 )#line:154
    @staticmethod #line:156
    def priGenFilePathByDateTime (O0000OOOO0OO0OOOO ):#line:157
        ""#line:163
        OOO0OO00O00O000O0 =os .path .splitext (O0000OOOO0OO0OOOO )#line:164
        OO00O0000O0O0O00O =OOO0OO00O00O000O0 [0 ]#line:165
        O0O0O0OO0OOOOOO00 =OOO0OO00O00O000O0 [-1 ]#line:166
        OOO0OO000OO000000 =datetime .date .today ().strftime ("%Y-%m-%d")#line:167
        return OO00O0000O0O0O00O +"_"+OOO0OO000OO000000 +O0O0O0OO0OOOOOO00 #line:168
if __name__ =='__main__':#line:171
    print (1 )#line:179
