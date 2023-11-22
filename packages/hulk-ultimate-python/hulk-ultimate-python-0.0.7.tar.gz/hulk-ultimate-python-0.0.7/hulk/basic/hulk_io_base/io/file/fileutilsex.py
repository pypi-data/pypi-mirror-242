import os #line:1
import shutil #line:2
import sys #line:3
import datetime #line:4
sys .path .append (os .getcwd ())#line:6
class FileUtilsEx :#line:9
    ""#line:10
    def __init__ (OO00O00O00O0OO0OO ):#line:12
        ""#line:13
    @staticmethod #line:15
    def delFile (OOOOO0O0O0O000O00 ):#line:16
        ""#line:21
        FileUtilsEx .priDelFile (OOOOO0O0O0O000O00 )#line:23
    @staticmethod #line:25
    def delFileAndCreateFileEmpty (O0OO00O0OOOOO000O ):#line:26
        ""#line:31
        FileUtilsEx .priDelFile (O0OO00O0OOOOO000O )#line:33
        FileUtilsEx .priCreateFileEmpty (O0OO00O0OOOOO000O )#line:35
    @staticmethod #line:37
    def writeAllText (O0O0OOOO00O0OO0O0 ,O0O0OOOO0O0O0O0O0 ):#line:38
        ""#line:44
        FileUtilsEx .delFileAndCreateFileEmpty (O0O0OOOO00O0OO0O0 )#line:45
        with open (O0O0OOOO00O0OO0O0 ,"w",encoding ="utf-8")as O0OO00OOO0OO00O00 :#line:46
            O0OO00OOO0OO00O00 .write (O0O0OOOO0O0O0O0O0 )#line:47
    @staticmethod #line:49
    def readAllText (OOO000OO0OO000O0O ):#line:50
        ""#line:55
        with open (OOO000OO0OO000O0O ,"r",encoding ="utf-8")as O0O0OO0OO0OO0O00O :#line:56
            O0OO0000OOOOO00OO =O0O0OO0OO0OO0O00O .read ()#line:57
        return O0OO0000OOOOO00OO #line:58
    @staticmethod #line:60
    def readAllLines (OOOO0000O0OO0O0OO ):#line:61
        ""#line:66
        O0000O0O0O00OOOOO =FileUtilsEx .readAllText (OOOO0000O0OO0O0OO )#line:67
        return O0000O0O0O00OOOOO .split ("\n")#line:68
    @staticmethod #line:70
    def appendFile (OOOOOO0O0000O000O ,OO000O000O0OOO000 ):#line:71
        ""#line:77
        FileUtilsEx .priCreateFileEmpty (OOOOOO0O0000O000O )#line:78
        with open (OOOOOO0O0000O000O ,"a",encoding ="utf-8")as O000O0000OOOO00O0 :#line:79
            O000O0000OOOO00O0 .write (OO000O000O0OOO000 )#line:80
    @staticmethod #line:82
    def appendFileWithDateTime (O000000000O0O0O00 ,O000O00O00O0OOO00 ):#line:83
        ""#line:89
        O00OOOOOO0O0O000O =FileUtilsEx .priGenFilePathByDateTime (O000000000O0O0O00 )#line:90
        FileUtilsEx .appendFile (O00OOOOOO0O0O000O ,O000O00O00O0OOO00 )#line:91
    @staticmethod #line:93
    def copyFile (OOO000O0000000OO0 ,OO0OO0000O00OO0OO ):#line:94
        ""#line:100
        FileUtilsEx .priCreateFileEmpty (OO0OO0000O00OO0OO )#line:103
        shutil .copy2 (OOO000O0000000OO0 ,OO0OO0000O00OO0OO )#line:105
    @staticmethod #line:107
    def iterAllFiles (O00OOO000O0OOOO0O ,O00O00O000OO0O0O0 ):#line:108
        ""#line:114
        for O00OO0O0OOO000000 ,O0O0OO000OO0O0OOO ,OOOO0OO0OO00O000O in os .walk (O00OOO000O0OOOO0O ):#line:115
            for OOO0O00O0OOO00OO0 in OOOO0OO0OO00O000O :#line:116
                if OOO0O00O0OOO00OO0 .endswith (O00O00O000OO0O0O0 ):#line:117
                    OO0O00000OOO0000O =os .path .join (O00OO0O0OOO000000 ,OOO0O00O0OOO00OO0 )#line:118
                    yield OO0O00000OOO0000O #line:119
    @staticmethod #line:121
    def priGetDirPath (O0OO0000O0OOO0000 ):#line:122
        ""#line:127
        return os .path .dirname (O0OO0000O0OOO0000 )#line:128
    @staticmethod #line:130
    def priCreateDirEmpty (O00O000000O00OOOO ):#line:131
        ""#line:136
        if not os .path .exists (O00O000000O00OOOO ):#line:137
            os .makedirs (O00O000000O00OOOO ,exist_ok =True )#line:138
    @staticmethod #line:140
    def priCreateFileEmpty (OO0OOO0O0OO0OO0OO ):#line:141
        ""#line:146
        OO0O0OOO000000OO0 =FileUtilsEx .priGetDirPath (OO0OOO0O0OO0OO0OO )#line:148
        FileUtilsEx .priCreateDirEmpty (OO0O0OOO000000OO0 )#line:150
        if not os .path .exists (OO0OOO0O0OO0OO0OO ):#line:152
            with open (OO0OOO0O0OO0OO0OO ,"w",encoding ="utf-8"):#line:153
                pass #line:154
    @staticmethod #line:156
    def priDelFile (OOOOOO0O000OOOOO0 ):#line:157
        ""#line:162
        if os .path .exists (OOOOOO0O000OOOOO0 ):#line:163
            os .remove (OOOOOO0O000OOOOO0 )#line:164
    @staticmethod #line:166
    def priGenFilePathByDateTime (O0OOO0O000O000OO0 ):#line:167
        ""#line:173
        O00OO00O000000O00 =os .path .splitext (O0OOO0O000O000OO0 )#line:174
        OO000O00O00O0O0OO =O00OO00O000000O00 [0 ]#line:175
        OOO0OO00OOO000OOO =O00OO00O000000O00 [-1 ]#line:176
        O0OO00O00O0OO0000 =datetime .date .today ().strftime ("%Y-%m-%d")#line:177
        return OO000O00O00O0O0OO +"_"+O0OO00O00O0OO0000 +OOO0OO00OOO000OOO #line:178
if __name__ =='__main__':#line:181
    print (1 )#line:189
