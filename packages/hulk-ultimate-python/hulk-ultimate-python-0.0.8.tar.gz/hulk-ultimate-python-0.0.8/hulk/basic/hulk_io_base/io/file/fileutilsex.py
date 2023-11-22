import os #line:1
import shutil #line:2
import sys #line:3
import datetime #line:4
sys .path .append (os .getcwd ())#line:6
class FileUtilsEx :#line:9
    ""#line:10
    def __init__ (OO0OOOOO00O0OOOO0 ):#line:12
        ""#line:13
    @staticmethod #line:15
    def delFile (O00O000O000OO0OO0 ):#line:16
        ""#line:21
        FileUtilsEx .priDelFile (O00O000O000OO0OO0 )#line:23
    @staticmethod #line:25
    def delFileAndCreateFileEmpty (O000O0000O0OOO000 ):#line:26
        ""#line:31
        FileUtilsEx .priDelFile (O000O0000O0OOO000 )#line:33
        FileUtilsEx .priCreateFileEmpty (O000O0000O0OOO000 )#line:35
    @staticmethod #line:37
    def writeAllText (O000OOOOO0O0OO00O ,O0000O0OO0OOOOO00 ):#line:38
        ""#line:44
        FileUtilsEx .delFileAndCreateFileEmpty (O000OOOOO0O0OO00O )#line:45
        with open (O000OOOOO0O0OO00O ,"w",encoding ="utf-8")as OOOO0OOOO000OOO00 :#line:46
            OOOO0OOOO000OOO00 .write (O0000O0OO0OOOOO00 )#line:47
    @staticmethod #line:49
    def readAllText (O00O00000O0O0OO00 ):#line:50
        ""#line:55
        with open (O00O00000O0O0OO00 ,"r",encoding ="utf-8")as OOOOO0OO00O000O00 :#line:56
            OO0O0O0O0OOOO00OO =OOOOO0OO00O000O00 .read ()#line:57
        return OO0O0O0O0OOOO00OO #line:58
    @staticmethod #line:60
    def readAllLines (O00OOO0O0OOOOO0OO ):#line:61
        ""#line:66
        OO0O000OO00O00O0O =FileUtilsEx .readAllText (O00OOO0O0OOOOO0OO )#line:67
        return OO0O000OO00O00O0O .split ("\n")#line:68
    @staticmethod #line:70
    def appendFile (O00OOOO0O00O0OOO0 ,OO00O0OOO000OO00O ):#line:71
        ""#line:77
        FileUtilsEx .priCreateFileEmpty (O00OOOO0O00O0OOO0 )#line:78
        with open (O00OOOO0O00O0OOO0 ,"a",encoding ="utf-8")as O0000000O0O0OOO0O :#line:79
            O0000000O0O0OOO0O .write (OO00O0OOO000OO00O )#line:80
    @staticmethod #line:82
    def appendFileWithDateTime (OOO0OOOOO0OOO0O00 ,O00O0OOOOOO0O00OO ):#line:83
        ""#line:89
        O00OOOO000O000000 =FileUtilsEx .priGenFilePathByDateTime (OOO0OOOOO0OOO0O00 )#line:90
        FileUtilsEx .appendFile (O00OOOO000O000000 ,O00O0OOOOOO0O00OO )#line:91
    @staticmethod #line:93
    def copyFile (OO000OO0O000OOO00 ,OOO00000O0O00O000 ):#line:94
        ""#line:100
        FileUtilsEx .priCreateFileEmpty (OOO00000O0O00O000 )#line:103
        shutil .copy2 (OO000OO0O000OOO00 ,OOO00000O0O00O000 )#line:105
    @staticmethod #line:107
    def iterAllFiles (O00O000O000000O0O ,OO00OO0OOO0OOOO00 ):#line:108
        ""#line:114
        for O0O000O000OOO0000 ,O0O000OOOO0OO0O0O ,OO0O0OOO00OO0OOO0 in os .walk (O00O000O000000O0O ):#line:115
            for OO0O0OO00O0O00000 in OO0O0OOO00OO0OOO0 :#line:116
                if OO0O0OO00O0O00000 .endswith (OO00OO0OOO0OOOO00 ):#line:117
                    OO00O000O0OOO00O0 =os .path .join (O0O000O000OOO0000 ,OO0O0OO00O0O00000 )#line:118
                    yield OO00O000O0OOO00O0 #line:119
    @staticmethod #line:121
    def priGetDirPath (O0OO0O00O0O0OO0O0 ):#line:122
        ""#line:127
        return os .path .dirname (O0OO0O00O0O0OO0O0 )#line:128
    @staticmethod #line:130
    def priCreateDirEmpty (O0OOOO0OOO00OOO0O ):#line:131
        ""#line:136
        if not os .path .exists (O0OOOO0OOO00OOO0O ):#line:137
            os .makedirs (O0OOOO0OOO00OOO0O ,exist_ok =True )#line:138
    @staticmethod #line:140
    def priCreateFileEmpty (OO0O0OOO00OOOO00O ):#line:141
        ""#line:146
        OO000000O0O0O00O0 =FileUtilsEx .priGetDirPath (OO0O0OOO00OOOO00O )#line:148
        FileUtilsEx .priCreateDirEmpty (OO000000O0O0O00O0 )#line:150
        if not os .path .exists (OO0O0OOO00OOOO00O ):#line:152
            with open (OO0O0OOO00OOOO00O ,"w",encoding ="utf-8"):#line:153
                pass #line:154
    @staticmethod #line:156
    def priDelFile (O0000OO0OOO00000O ):#line:157
        ""#line:162
        if os .path .exists (O0000OO0OOO00000O ):#line:163
            os .remove (O0000OO0OOO00000O )#line:164
    @staticmethod #line:166
    def priGenFilePathByDateTime (OOOO00000000OOOOO ):#line:167
        ""#line:173
        OOOOO00O0OO000000 =os .path .splitext (OOOO00000000OOOOO )#line:174
        O0000O0OOO0OO0000 =OOOOO00O0OO000000 [0 ]#line:175
        OO000O0O0OO0O0OO0 =OOOOO00O0OO000000 [-1 ]#line:176
        O0OO000O000OO000O =datetime .date .today ().strftime ("%Y-%m-%d")#line:177
        return O0000O0OOO0OO0000 +"_"+O0OO000O000OO000O +OO000O0O0OO0O0OO0 #line:178
if __name__ =='__main__':#line:181
    print (1 )#line:189
