import os #line:1
import shutil #line:2
import sys #line:3
import datetime #line:4
sys .path .append (os .getcwd ())#line:6
class FileUtilsEx :#line:9
    ""#line:10
    def __init__ (OOOO0O0OOOO000OOO ):#line:12
        ""#line:13
    @staticmethod #line:15
    def delFile (O0O0OO00OOO0O0000 ):#line:16
        ""#line:21
        FileUtilsEx .priDelFile (O0O0OO00OOO0O0000 )#line:23
    @staticmethod #line:25
    def delFileAndCreateFileEmpty (O0OO000OO00O00O00 ):#line:26
        ""#line:31
        FileUtilsEx .priDelFile (O0OO000OO00O00O00 )#line:33
        FileUtilsEx .priCreateFileEmpty (O0OO000OO00O00O00 )#line:35
    @staticmethod #line:37
    def writeAllText (OOO00O000O0OOOO0O ,O0O0OOOOOOO0O0OO0 ):#line:38
        ""#line:44
        FileUtilsEx .delFileAndCreateFileEmpty (OOO00O000O0OOOO0O )#line:45
        with open (OOO00O000O0OOOO0O ,"w",encoding ="utf-8")as O0O0OOOO0O0OO00OO :#line:46
            O0O0OOOO0O0OO00OO .write (O0O0OOOOOOO0O0OO0 )#line:47
    @staticmethod #line:49
    def readAllText (OO0OOO00OO0O0000O ):#line:50
        ""#line:55
        with open (OO0OOO00OO0O0000O ,"r",encoding ="utf-8")as O0O00O0OOO0OO000O :#line:56
            O0O00O00O0000OO00 =O0O00O0OOO0OO000O .read ()#line:57
        return O0O00O00O0000OO00 #line:58
    @staticmethod #line:60
    def readAllLines (O0000O00OO000OOOO ):#line:61
        ""#line:66
        OO00OO0OOOOO00OO0 =FileUtilsEx .readAllText (O0000O00OO000OOOO )#line:67
        return OO00OO0OOOOO00OO0 .split ("\n")#line:68
    @staticmethod #line:70
    def appendFile (OOOOOO00OOO000O00 ,OOOOO0OO0OOOO0OO0 ):#line:71
        ""#line:77
        FileUtilsEx .priCreateFileEmpty (OOOOOO00OOO000O00 )#line:78
        with open (OOOOOO00OOO000O00 ,"a",encoding ="utf-8")as OOO00000O0OOO0000 :#line:79
            OOO00000O0OOO0000 .write (OOOOO0OO0OOOO0OO0 )#line:80
    @staticmethod #line:82
    def appendFileWithDateTime (O0000OO0OOO0O0OO0 ,O00O0OO00OO0OOOOO ):#line:83
        ""#line:89
        O0O0O0O000OOOOO0O =FileUtilsEx .priGenFilePathByDateTime (O0000OO0OOO0O0OO0 )#line:90
        FileUtilsEx .appendFile (O0O0O0O000OOOOO0O ,O00O0OO00OO0OOOOO )#line:91
    @staticmethod #line:93
    def copyFile (O00O0O0OOO00OOOOO ,O0O00OO000O000O0O ):#line:94
        ""#line:100
        FileUtilsEx .priCreateFileEmpty (O0O00OO000O000O0O )#line:103
        shutil .copy2 (O00O0O0OOO00OOOOO ,O0O00OO000O000O0O )#line:105
    @staticmethod #line:107
    def iterAllFiles (OOOOO0O00O0O0O0OO ,OO00OO00OO00000OO ):#line:108
        ""#line:114
        for OO0O0OOOO0OO0OO00 ,O0O0000OO0O00O0O0 ,OOOOOOOO0000000OO in os .walk (OOOOO0O00O0O0O0OO ):#line:115
            for OO0O000O0O0O000OO in OOOOOOOO0000000OO :#line:116
                if OO0O000O0O0O000OO .endswith (OO00OO00OO00000OO ):#line:117
                    OO00O0OO0OOO0OO0O =os .path .join (OO0O0OOOO0OO0OO00 ,OO0O000O0O0O000OO )#line:118
                    yield OO00O0OO0OOO0OO0O #line:119
    @staticmethod #line:121
    def priGetDirPath (O0000000O00OO0OOO ):#line:122
        ""#line:127
        return os .path .dirname (O0000000O00OO0OOO )#line:128
    @staticmethod #line:130
    def priCreateDirEmpty (OO000O0OO000O00OO ):#line:131
        ""#line:136
        if not os .path .exists (OO000O0OO000O00OO ):#line:137
            os .makedirs (OO000O0OO000O00OO ,exist_ok =True )#line:138
    @staticmethod #line:140
    def priCreateFileEmpty (O0O00O000O0O000O0 ):#line:141
        ""#line:146
        OO0OOO00O00OOOOO0 =FileUtilsEx .priGetDirPath (O0O00O000O0O000O0 )#line:148
        FileUtilsEx .priCreateDirEmpty (OO0OOO00O00OOOOO0 )#line:150
        if not os .path .exists (O0O00O000O0O000O0 ):#line:152
            with open (O0O00O000O0O000O0 ,"w",encoding ="utf-8"):#line:153
                pass #line:154
    @staticmethod #line:156
    def priDelFile (OO0OO0OOOO00OOOOO ):#line:157
        ""#line:162
        if os .path .exists (OO0OO0OOOO00OOOOO ):#line:163
            os .remove (OO0OO0OOOO00OOOOO )#line:164
    @staticmethod #line:166
    def priGenFilePathByDateTime (OO0000O00O00O0OOO ):#line:167
        ""#line:173
        O0O000O00O0O0OO0O =os .path .splitext (OO0000O00O00O0OOO )#line:174
        OOO0OOO0OOOO0OO00 =O0O000O00O0O0OO0O [0 ]#line:175
        OO00O000O00OO000O =O0O000O00O0O0OO0O [-1 ]#line:176
        O000O0000O000O000 =datetime .date .today ().strftime ("%Y-%m-%d")#line:177
        return OOO0OOO0OOOO0OO00 +"_"+O000O0000O000O000 +OO00O000O00OO000O #line:178
if __name__ =='__main__':#line:181
    print (1 )#line:189
