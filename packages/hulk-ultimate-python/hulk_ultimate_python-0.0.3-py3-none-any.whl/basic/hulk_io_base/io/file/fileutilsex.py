import os #line:1
import shutil #line:2
import sys #line:3
import datetime #line:4
sys .path .append (os .getcwd ())#line:6
class FileUtilsEx :#line:9
    ""#line:10
    def __init__ (O00O0OO00OO0O0000 ):#line:12
        ""#line:13
    @staticmethod #line:15
    def delFileAndCreateFileEmpty (O0OOOO00O0O0O0O00 ):#line:16
        ""#line:21
        FileUtilsEx .priDelFile (O0OOOO00O0O0O0O00 )#line:23
        FileUtilsEx .priCreateFileEmpty (O0OOOO00O0O0O0O00 )#line:25
    @staticmethod #line:27
    def writeAllText (O0O00000OO0OO0OO0 ,O00O0O00O0OOOO0O0 ):#line:28
        ""#line:34
        FileUtilsEx .delFileAndCreateFileEmpty (O0O00000OO0OO0OO0 )#line:35
        with open (O0O00000OO0OO0OO0 ,"w",encoding ="utf-8")as OO0OO0O000000O0O0 :#line:36
            OO0OO0O000000O0O0 .write (O00O0O00O0OOOO0O0 )#line:37
    @staticmethod #line:39
    def readAllText (OO0O000000OO00O00 ):#line:40
        ""#line:45
        with open (OO0O000000OO00O00 ,"r",encoding ="utf-8")as OOOOOOO0OO000O0O0 :#line:46
            OOO00OO00OOOO00OO =OOOOOOO0OO000O0O0 .read ()#line:47
        return OOO00OO00OOOO00OO #line:48
    @staticmethod #line:50
    def readAllLines (O0O00O0OO0O0O000O ):#line:51
        ""#line:56
        OOOOO0OO0OOOOOOOO =FileUtilsEx .readAllText (O0O00O0OO0O0O000O )#line:57
        return OOOOO0OO0OOOOOOOO .split ("\n")#line:58
    @staticmethod #line:60
    def appendFile (O00OO0OO00OOO0O00 ,O000OOO0000OO0OO0 ):#line:61
        ""#line:67
        FileUtilsEx .priCreateFileEmpty (O00OO0OO00OOO0O00 )#line:68
        with open (O00OO0OO00OOO0O00 ,"a",encoding ="utf-8")as OO0O00OO0O0OOOO00 :#line:69
            OO0O00OO0O0OOOO00 .write (O000OOO0000OO0OO0 )#line:70
    @staticmethod #line:72
    def appendFileWithDateTime (OOO000O0O000OOO0O ,OOOO0OO000000O000 ):#line:73
        ""#line:79
        OO0O0O00OOOO0OO00 =FileUtilsEx .priGenFilePathByDateTime (OOO000O0O000OOO0O )#line:80
        FileUtilsEx .appendFile (OO0O0O00OOOO0OO00 ,OOOO0OO000000O000 )#line:81
    @staticmethod #line:83
    def copyFile (OO0O00OOO0OO00000 ,OO00O0O0O000O00OO ):#line:84
        ""#line:90
        FileUtilsEx .priCreateFileEmpty (OO00O0O0O000O00OO )#line:93
        shutil .copy2 (OO0O00OOO0OO00000 ,OO00O0O0O000O00OO )#line:95
    @staticmethod #line:97
    def iterAllFiles (OOOO0O0O000O000OO ,OOO00O0O0O0O00O0O ):#line:98
        ""#line:104
        for O00O0000O0OOO0OOO ,OO00OOO0O00O0O0O0 ,O00O0O0OO000O0OO0 in os .walk (OOOO0O0O000O000OO ):#line:105
            for O00OO0OO000O0O0OO in O00O0O0OO000O0OO0 :#line:106
                if O00OO0OO000O0O0OO .endswith (OOO00O0O0O0O00O0O ):#line:107
                    O0O0OOOOOOO000OOO =os .path .join (O00O0000O0OOO0OOO ,O00OO0OO000O0O0OO )#line:108
                    yield O0O0OOOOOOO000OOO #line:109
    @staticmethod #line:111
    def priGetDirPath (O0OO000000O0000OO ):#line:112
        ""#line:117
        return os .path .dirname (O0OO000000O0000OO )#line:118
    @staticmethod #line:120
    def priCreateDirEmpty (O00OO00O0O000O000 ):#line:121
        ""#line:126
        if not os .path .exists (O00OO00O0O000O000 ):#line:127
            os .makedirs (O00OO00O0O000O000 ,exist_ok =True )#line:128
    @staticmethod #line:130
    def priCreateFileEmpty (OO0O0000O0OO00000 ):#line:131
        ""#line:136
        O00OO00O000O000O0 =FileUtilsEx .priGetDirPath (OO0O0000O0OO00000 )#line:138
        FileUtilsEx .priCreateDirEmpty (O00OO00O000O000O0 )#line:140
        if not os .path .exists (OO0O0000O0OO00000 ):#line:142
            with open (OO0O0000O0OO00000 ,"w",encoding ="utf-8"):#line:143
                pass #line:144
    @staticmethod #line:146
    def priDelFile (O0OO0O00OOOO00O0O ):#line:147
        ""#line:152
        if os .path .exists (O0OO0O00OOOO00O0O ):#line:153
            os .remove (O0OO0O00OOOO00O0O )#line:154
    @staticmethod #line:156
    def priGenFilePathByDateTime (O0O0OOOO000OO0OO0 ):#line:157
        ""#line:163
        O0OOOO000O0OOOO00 =os .path .splitext (O0O0OOOO000OO0OO0 )#line:164
        OOOO00O0OO0O0O0O0 =O0OOOO000O0OOOO00 [0 ]#line:165
        O0000OO00O0OOOOOO =O0OOOO000O0OOOO00 [-1 ]#line:166
        O00O00OOO0O0OOO0O =datetime .date .today ().strftime ("%Y-%m-%d")#line:167
        return OOOO00O0OO0O0O0O0 +"_"+O00O00OOO0O0OOO0O +O0000OO00O0OOOOOO #line:168
if __name__ =='__main__':#line:171
    print (1 )#line:179
