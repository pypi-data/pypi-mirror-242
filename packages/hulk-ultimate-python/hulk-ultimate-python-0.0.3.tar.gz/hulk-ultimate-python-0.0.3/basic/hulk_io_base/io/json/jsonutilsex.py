import json #line:1
from basic import FileUtilsEx #line:3
class JsonUtilsEx :#line:6
    ""#line:7
    def __init__ (OOOO0OOOOO0OOOOO0 ):#line:9
        ""#line:10
    @staticmethod #line:12
    def toPythonObjFromFile (O0OOO000O000OOO0O ):#line:13
        ""#line:18
        with open (O0OOO000O000OOO0O ,encoding ="utf-8")as O000OO00O0O0000OO :#line:19
            OO0000O00OOOOO0OO =json .load (O000OO00O0O0000OO )#line:20
        return OO0000O00OOOOO0OO #line:21
    @staticmethod #line:23
    def toStrByFile (OO00000O0O000000O ,O00000O0OOO0OO0O0 ):#line:24
        ""#line:30
        OOOOO0O0OO0OO00O0 =json .dumps (O00000O0OOO0OO0O0 ,ensure_ascii =False )#line:31
        FileUtilsEx .writeAllText (OO00000O0O000000O ,OOOOO0O0OO0OO00O0 )#line:32
