import json #line:1
from hulk import FileUtilsEx #line:3
class JsonUtilsEx :#line:6
    ""#line:7
    def __init__ (OO00000O00000000O ):#line:9
        ""#line:10
    @staticmethod #line:12
    def toPythonObjFromFile (OOO00O0OOO00O0000 ):#line:13
        ""#line:18
        with open (OOO00O0OOO00O0000 ,encoding ="utf-8")as OO0O0OOOO00OOO000 :#line:19
            O0OOOO0O000O00O00 =json .load (OO0O0OOOO00OOO000 )#line:20
        return O0OOOO0O000O00O00 #line:21
    @staticmethod #line:23
    def toStrByFile (OO0O000O00OO00O0O ,O0OO000O0O00O0000 ):#line:24
        ""#line:30
        OO00000OOO0OO0O0O =json .dumps (O0OO000O0O00O0000 ,ensure_ascii =False )#line:31
        FileUtilsEx .writeAllText (OO0O000O00OO00O0O ,OO00000OOO0OO0O0O )#line:32
