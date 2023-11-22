import os #line:1
import shutil #line:2
import sys #line:3
import datetime #line:4
sys .path .append (os .getcwd ())#line:6
class FileUtilsEx :#line:9
    ""#line:10
    def __init__ (OO00OO00OOOO00O00 ):#line:12
        ""#line:13
    @staticmethod #line:15
    def delFile (O00OOOO00OOO000OO ):#line:16
        ""#line:21
        FileUtilsEx .priDelFile (O00OOOO00OOO000OO )#line:23
    @staticmethod #line:25
    def delFileAndCreateFileEmpty (O00OO0O0OOOOO0OOO ):#line:26
        ""#line:31
        FileUtilsEx .priDelFile (O00OO0O0OOOOO0OOO )#line:33
        FileUtilsEx .priCreateFileEmpty (O00OO0O0OOOOO0OOO )#line:35
    @staticmethod #line:37
    def writeAllText (OOO0OO0OO000OOO00 ,O0000OOOO0OO00OOO ):#line:38
        ""#line:44
        FileUtilsEx .delFileAndCreateFileEmpty (OOO0OO0OO000OOO00 )#line:45
        with open (OOO0OO0OO000OOO00 ,"w",encoding ="utf-8")as O0000O0OO0O00OO0O :#line:46
            O0000O0OO0O00OO0O .write (O0000OOOO0OO00OOO )#line:47
    @staticmethod #line:49
    def readAllText (O0O0O0O0O0O000O00 ):#line:50
        ""#line:55
        with open (O0O0O0O0O0O000O00 ,"r",encoding ="utf-8")as O0O0OO00OOO00O00O :#line:56
            O00OOO000OOOOO000 =O0O0OO00OOO00O00O .read ()#line:57
        return O00OOO000OOOOO000 #line:58
    @staticmethod #line:60
    def readAllLines (OO00OOOOO000OOOOO ):#line:61
        ""#line:66
        O000O0000O00OO000 =FileUtilsEx .readAllText (OO00OOOOO000OOOOO )#line:67
        return O000O0000O00OO000 .split ("\n")#line:68
    @staticmethod #line:70
    def appendFile (OOO00O0OO00OOO00O ,OO0O00O0OOO0OOO0O ):#line:71
        ""#line:77
        FileUtilsEx .priCreateFileEmpty (OOO00O0OO00OOO00O )#line:78
        with open (OOO00O0OO00OOO00O ,"a",encoding ="utf-8")as O0O0OOO0OO0O0O000 :#line:79
            O0O0OOO0OO0O0O000 .write (OO0O00O0OOO0OOO0O )#line:80
    @staticmethod #line:82
    def appendFileWithDateTime (O0OOOOO00OO0OOO00 ,O000O0OO000OO0000 ):#line:83
        ""#line:89
        O0OOO00OOOO0OOO00 =FileUtilsEx .priGenFilePathByDateTime (O0OOOOO00OO0OOO00 )#line:90
        FileUtilsEx .appendFile (O0OOO00OOOO0OOO00 ,O000O0OO000OO0000 )#line:91
    @staticmethod #line:93
    def copyFile (O0OO0000O0OOO0O00 ,O0OO0O0000OO00O0O ):#line:94
        ""#line:100
        FileUtilsEx .priCreateFileEmpty (O0OO0O0000OO00O0O )#line:103
        shutil .copy2 (O0OO0000O0OOO0O00 ,O0OO0O0000OO00O0O )#line:105
    @staticmethod #line:107
    def iterAllFiles (O0O000OO0000OOOO0 ,O0O0OO0OOO0OOOOOO ):#line:108
        ""#line:114
        for O0O0000O00000O0O0 ,O00OOO000OO0OOO0O ,OOO000OOO0OOO0000 in os .walk (O0O000OO0000OOOO0 ):#line:115
            for O0O000O000OOO00O0 in OOO000OOO0OOO0000 :#line:116
                if O0O000O000OOO00O0 .endswith (O0O0OO0OOO0OOOOOO ):#line:117
                    OO0O0OOOOOO0OOO00 =os .path .join (O0O0000O00000O0O0 ,O0O000O000OOO00O0 )#line:118
                    yield OO0O0OOOOOO0OOO00 #line:119
    @staticmethod #line:121
    def priGetDirPath (OOOOO0OO0OO000OOO ):#line:122
        ""#line:127
        return os .path .dirname (OOOOO0OO0OO000OOO )#line:128
    @staticmethod #line:130
    def priCreateDirEmpty (O0O00O0OOO0000OO0 ):#line:131
        ""#line:136
        if not os .path .exists (O0O00O0OOO0000OO0 ):#line:137
            os .makedirs (O0O00O0OOO0000OO0 ,exist_ok =True )#line:138
    @staticmethod #line:140
    def priCreateFileEmpty (O00OO0O0O00OOO000 ):#line:141
        ""#line:146
        OO0O00O0O000OO0O0 =FileUtilsEx .priGetDirPath (O00OO0O0O00OOO000 )#line:148
        FileUtilsEx .priCreateDirEmpty (OO0O00O0O000OO0O0 )#line:150
        if not os .path .exists (O00OO0O0O00OOO000 ):#line:152
            with open (O00OO0O0O00OOO000 ,"w",encoding ="utf-8"):#line:153
                pass #line:154
    @staticmethod #line:156
    def priDelFile (O000OOOOO00O00000 ):#line:157
        ""#line:162
        if os .path .exists (O000OOOOO00O00000 ):#line:163
            os .remove (O000OOOOO00O00000 )#line:164
    @staticmethod #line:166
    def priGenFilePathByDateTime (O0OO0O00OOO0OOO00 ):#line:167
        ""#line:173
        O00O00O00O000O000 =os .path .splitext (O0OO0O00OOO0OOO00 )#line:174
        OOOO0OO00OO0O0O00 =O00O00O00O000O000 [0 ]#line:175
        O00O00O0OOO0OO00O =O00O00O00O000O000 [-1 ]#line:176
        OO0O0OO0O0O00OOOO =datetime .date .today ().strftime ("%Y-%m-%d")#line:177
        return OOOO0OO00OO0O0O00 +"_"+OO0O0OO0O0O00OOOO +O00O00O0OOO0OO00O #line:178
if __name__ =='__main__':#line:181
    print (1 )#line:189
