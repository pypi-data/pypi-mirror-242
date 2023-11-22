import json #line:1
from hulk import FileUtilsEx #line:3
class JsonUtilsEx :#line:6
    ""#line:7
    def __init__ (OOOO000O00OO0O00O ):#line:9
        ""#line:10
    @staticmethod #line:12
    def toPythonObjFromFile (OOOOOOOOOO0OOOOOO ):#line:13
        ""#line:18
        with open (OOOOOOOOOO0OOOOOO ,encoding ="utf-8")as O000O000O0000000O :#line:19
            OOO00OO00OO0O0O00 =json .load (O000O000O0000000O )#line:20
        return OOO00OO00OO0O0O00 #line:21
    @staticmethod #line:23
    def toStrByFile (OO00OOOO00O00OO0O ,OOOO00O0O00O00O00 ):#line:24
        ""#line:30
        O00O0O0000OOO0O0O =json .dumps (OOOO00O0O00O00O00 ,ensure_ascii =False )#line:31
        FileUtilsEx .writeAllText (OO00OOOO00O00OO0O ,O00O0O0000OOO0O0O )#line:32
