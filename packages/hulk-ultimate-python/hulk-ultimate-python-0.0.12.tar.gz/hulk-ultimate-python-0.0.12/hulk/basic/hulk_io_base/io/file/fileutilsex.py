import os #line:1
import shutil #line:2
import sys #line:3
import datetime #line:4
sys .path .append (os .getcwd ())#line:6
class FileUtilsEx :#line:9
    ""#line:10
    def __init__ (O000000OO00000O00 ):#line:12
        ""#line:13
    @staticmethod #line:15
    def delFile (O0O0OOOOO00OO0OOO ):#line:16
        ""#line:21
        FileUtilsEx .priDelFile (O0O0OOOOO00OO0OOO )#line:23
    @staticmethod #line:25
    def delFileAndCreateFileEmpty (OOOOO0O0O0000OOO0 ):#line:26
        ""#line:31
        FileUtilsEx .priDelFile (OOOOO0O0O0000OOO0 )#line:33
        FileUtilsEx .priCreateFileEmpty (OOOOO0O0O0000OOO0 )#line:35
    @staticmethod #line:37
    def writeAllText (OO000O0O0OO0OOOO0 ,OOO0OO0000O00O0O0 ):#line:38
        ""#line:44
        FileUtilsEx .delFileAndCreateFileEmpty (OO000O0O0OO0OOOO0 )#line:45
        with open (OO000O0O0OO0OOOO0 ,"w",encoding ="utf-8")as O00OO00000000OO00 :#line:46
            O00OO00000000OO00 .write (OOO0OO0000O00O0O0 )#line:47
    @staticmethod #line:49
    def readAllText (OO0O0OO00OO0OOOO0 ):#line:50
        ""#line:55
        with open (OO0O0OO00OO0OOOO0 ,"r",encoding ="utf-8")as O00000O00O0O0OO0O :#line:56
            OO000OO0OOOO00OO0 =O00000O00O0O0OO0O .read ()#line:57
        return OO000OO0OOOO00OO0 #line:58
    @staticmethod #line:60
    def readAllLines (O000O00000000O0OO ):#line:61
        ""#line:66
        OO00O00OO0OO00OO0 =FileUtilsEx .readAllText (O000O00000000O0OO )#line:67
        return OO00O00OO0OO00OO0 .split ("\n")#line:68
    @staticmethod #line:70
    def appendFile (OOOO0O00OO0OO000O ,O00OOO0O0OO000OOO ):#line:71
        ""#line:77
        FileUtilsEx .priCreateFileEmpty (OOOO0O00OO0OO000O )#line:78
        with open (OOOO0O00OO0OO000O ,"a",encoding ="utf-8")as O00OOO0000000O0OO :#line:79
            O00OOO0000000O0OO .write (O00OOO0O0OO000OOO )#line:80
    @staticmethod #line:82
    def appendFileWithDateTime (OO0OOO00OO000000O ,O0O0OO0O0OO000OO0 ):#line:83
        ""#line:89
        O0OO0O0OOOOOO0000 =FileUtilsEx .priGenFilePathByDateTime (OO0OOO00OO000000O )#line:90
        FileUtilsEx .appendFile (O0OO0O0OOOOOO0000 ,O0O0OO0O0OO000OO0 )#line:91
    @staticmethod #line:93
    def copyFile (O00O00OO00O0OOO00 ,OOOO0O00OO0OO0OO0 ):#line:94
        ""#line:100
        FileUtilsEx .priCreateFileEmpty (OOOO0O00OO0OO0OO0 )#line:103
        shutil .copy2 (O00O00OO00O0OOO00 ,OOOO0O00OO0OO0OO0 )#line:105
    @staticmethod #line:107
    def iterAllFiles (OO00OOO00OO0O000O ,OOOOO0O00O0OO00OO ):#line:108
        ""#line:114
        for OO00O00O00O00O0O0 ,OO0OOO000OOO0OOOO ,O000O0000OOOOOOOO in os .walk (OO00OOO00OO0O000O ):#line:115
            for O00O00O000OOO0OO0 in O000O0000OOOOOOOO :#line:116
                if O00O00O000OOO0OO0 .endswith (OOOOO0O00O0OO00OO ):#line:117
                    O00O0O0O0O0OOOO0O =os .path .join (OO00O00O00O00O0O0 ,O00O00O000OOO0OO0 )#line:118
                    yield O00O0O0O0O0OOOO0O #line:119
    @staticmethod #line:121
    def priGetDirPath (O0O0OOO000OOOO0OO ):#line:122
        ""#line:127
        return os .path .dirname (O0O0OOO000OOOO0OO )#line:128
    @staticmethod #line:130
    def priCreateDirEmpty (O0O00OO0OO0O00O00 ):#line:131
        ""#line:136
        if not os .path .exists (O0O00OO0OO0O00O00 ):#line:137
            os .makedirs (O0O00OO0OO0O00O00 ,exist_ok =True )#line:138
    @staticmethod #line:140
    def priCreateFileEmpty (OOOO00000OO00OO00 ):#line:141
        ""#line:146
        OOO000000OOO0O00O =FileUtilsEx .priGetDirPath (OOOO00000OO00OO00 )#line:148
        FileUtilsEx .priCreateDirEmpty (OOO000000OOO0O00O )#line:150
        if not os .path .exists (OOOO00000OO00OO00 ):#line:152
            with open (OOOO00000OO00OO00 ,"w",encoding ="utf-8"):#line:153
                pass #line:154
    @staticmethod #line:156
    def priDelFile (O0O0OO000O0OOOO0O ):#line:157
        ""#line:162
        if os .path .exists (O0O0OO000O0OOOO0O ):#line:163
            os .remove (O0O0OO000O0OOOO0O )#line:164
    @staticmethod #line:166
    def priGenFilePathByDateTime (OO0OOO0OOOO000O00 ):#line:167
        ""#line:173
        O0O000OO00O00OO0O =os .path .splitext (OO0OOO0OOOO000O00 )#line:174
        O0OOOO0OOOOO0OO00 =O0O000OO00O00OO0O [0 ]#line:175
        OO00O0O0000O0000O =O0O000OO00O00OO0O [-1 ]#line:176
        O0O00OOOO0O00OOOO =datetime .date .today ().strftime ("%Y-%m-%d")#line:177
        return O0OOOO0OOOOO0OO00 +"_"+O0O00OOOO0O00OOOO +OO00O0O0000O0000O #line:178
if __name__ =='__main__':#line:181
    print (1 )#line:189
