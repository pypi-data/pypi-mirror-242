import json #line:1
from hulk import FileUtilsEx #line:3
class JsonUtilsEx :#line:6
    ""#line:7
    def __init__ (OOOO000000O00O0O0 ):#line:9
        ""#line:10
    @staticmethod #line:12
    def toPythonObjFromFile (O000OO0O0O0O0O0OO ):#line:13
        ""#line:18
        with open (O000OO0O0O0O0O0OO ,encoding ="utf-8")as OO0O000O0OO0OO000 :#line:19
            O000O00O0OOOOO0OO =json .load (OO0O000O0OO0OO000 )#line:20
        return O000O00O0OOOOO0OO #line:21
    @staticmethod #line:23
    def toStrByFile (OO0OOO000O0O0O00O ,O0OO00OOOO00000O0 ):#line:24
        ""#line:30
        OOO00O00000O0O00O =json .dumps (O0OO00OOOO00000O0 ,ensure_ascii =False )#line:31
        FileUtilsEx .writeAllText (OO0OOO000O0O0O00O ,OOO00O00000O0O00O )#line:32
