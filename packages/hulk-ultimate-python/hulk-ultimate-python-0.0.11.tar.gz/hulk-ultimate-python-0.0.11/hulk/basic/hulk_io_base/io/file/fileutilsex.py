import os #line:1
import shutil #line:2
import sys #line:3
import datetime #line:4
sys .path .append (os .getcwd ())#line:6
class FileUtilsEx :#line:9
    ""#line:10
    def __init__ (O000OOOO000OO0O0O ):#line:12
        ""#line:13
    @staticmethod #line:15
    def delFile (O00OO00000O0OO000 ):#line:16
        ""#line:21
        FileUtilsEx .priDelFile (O00OO00000O0OO000 )#line:23
    @staticmethod #line:25
    def delFileAndCreateFileEmpty (OOO0OO0000000OOOO ):#line:26
        ""#line:31
        FileUtilsEx .priDelFile (OOO0OO0000000OOOO )#line:33
        FileUtilsEx .priCreateFileEmpty (OOO0OO0000000OOOO )#line:35
    @staticmethod #line:37
    def writeAllText (OOOO00O0OOO00O000 ,O00O00O000O0OO0OO ):#line:38
        ""#line:44
        FileUtilsEx .delFileAndCreateFileEmpty (OOOO00O0OOO00O000 )#line:45
        with open (OOOO00O0OOO00O000 ,"w",encoding ="utf-8")as OOO0O00O00OOOO0O0 :#line:46
            OOO0O00O00OOOO0O0 .write (O00O00O000O0OO0OO )#line:47
    @staticmethod #line:49
    def readAllText (OO0O00OOO00OOO000 ):#line:50
        ""#line:55
        with open (OO0O00OOO00OOO000 ,"r",encoding ="utf-8")as OO00000OO0O00OO0O :#line:56
            O0O0O00OOO000OO00 =OO00000OO0O00OO0O .read ()#line:57
        return O0O0O00OOO000OO00 #line:58
    @staticmethod #line:60
    def readAllLines (O00O000OOOO0OOOOO ):#line:61
        ""#line:66
        OOO0O0O00O0000O00 =FileUtilsEx .readAllText (O00O000OOOO0OOOOO )#line:67
        return OOO0O0O00O0000O00 .split ("\n")#line:68
    @staticmethod #line:70
    def appendFile (O0O00OOO00O00OOOO ,OO000O0O00OO0O0OO ):#line:71
        ""#line:77
        FileUtilsEx .priCreateFileEmpty (O0O00OOO00O00OOOO )#line:78
        with open (O0O00OOO00O00OOOO ,"a",encoding ="utf-8")as O0OO0OO0OOO0O0OOO :#line:79
            O0OO0OO0OOO0O0OOO .write (OO000O0O00OO0O0OO )#line:80
    @staticmethod #line:82
    def appendFileWithDateTime (OOOOOOOOOOO0O0O0O ,O0000OOOOOO0O0O0O ):#line:83
        ""#line:89
        O0000O0O0O00O0000 =FileUtilsEx .priGenFilePathByDateTime (OOOOOOOOOOO0O0O0O )#line:90
        FileUtilsEx .appendFile (O0000O0O0O00O0000 ,O0000OOOOOO0O0O0O )#line:91
    @staticmethod #line:93
    def copyFile (OO0OO0OO00000OO00 ,O0O0OO00OO00OOOOO ):#line:94
        ""#line:100
        FileUtilsEx .priCreateFileEmpty (O0O0OO00OO00OOOOO )#line:103
        shutil .copy2 (OO0OO0OO00000OO00 ,O0O0OO00OO00OOOOO )#line:105
    @staticmethod #line:107
    def iterAllFiles (O0OO00OOO0OO0O0OO ,O0OOOOOO0OOO00O00 ):#line:108
        ""#line:114
        for OOO0OOO00OOO00O00 ,OO0000O0OO00O00OO ,OOO000000O000O000 in os .walk (O0OO00OOO0OO0O0OO ):#line:115
            for OO0OOOOO00OO00OO0 in OOO000000O000O000 :#line:116
                if OO0OOOOO00OO00OO0 .endswith (O0OOOOOO0OOO00O00 ):#line:117
                    O00OO0OO0000O00O0 =os .path .join (OOO0OOO00OOO00O00 ,OO0OOOOO00OO00OO0 )#line:118
                    yield O00OO0OO0000O00O0 #line:119
    @staticmethod #line:121
    def priGetDirPath (O0O000O00OOOOO00O ):#line:122
        ""#line:127
        return os .path .dirname (O0O000O00OOOOO00O )#line:128
    @staticmethod #line:130
    def priCreateDirEmpty (O00000O0O0OOO00OO ):#line:131
        ""#line:136
        if not os .path .exists (O00000O0O0OOO00OO ):#line:137
            os .makedirs (O00000O0O0OOO00OO ,exist_ok =True )#line:138
    @staticmethod #line:140
    def priCreateFileEmpty (O0O0000O00O000O00 ):#line:141
        ""#line:146
        OOO0OO0O000O0O0OO =FileUtilsEx .priGetDirPath (O0O0000O00O000O00 )#line:148
        FileUtilsEx .priCreateDirEmpty (OOO0OO0O000O0O0OO )#line:150
        if not os .path .exists (O0O0000O00O000O00 ):#line:152
            with open (O0O0000O00O000O00 ,"w",encoding ="utf-8"):#line:153
                pass #line:154
    @staticmethod #line:156
    def priDelFile (O0O0OOOOO0O0O00OO ):#line:157
        ""#line:162
        if os .path .exists (O0O0OOOOO0O0O00OO ):#line:163
            os .remove (O0O0OOOOO0O0O00OO )#line:164
    @staticmethod #line:166
    def priGenFilePathByDateTime (OOO0OO0OOO00O00OO ):#line:167
        ""#line:173
        O000OOO0OOO0OOOOO =os .path .splitext (OOO0OO0OOO00O00OO )#line:174
        O0OOOOO0OO0OOO0OO =O000OOO0OOO0OOOOO [0 ]#line:175
        OOO0000O000OO00O0 =O000OOO0OOO0OOOOO [-1 ]#line:176
        O0OO0000O0O0O0OOO =datetime .date .today ().strftime ("%Y-%m-%d")#line:177
        return O0OOOOO0OO0OOO0OO +"_"+O0OO0000O0O0O0OOO +OOO0000O000OO00O0 #line:178
if __name__ =='__main__':#line:181
    print (1 )#line:189
