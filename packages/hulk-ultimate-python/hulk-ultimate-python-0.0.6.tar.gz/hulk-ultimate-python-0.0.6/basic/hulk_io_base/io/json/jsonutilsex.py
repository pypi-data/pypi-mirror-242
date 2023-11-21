import json #line:1
from basic import FileUtilsEx #line:3
class JsonUtilsEx :#line:6
    ""#line:7
    def __init__ (O00OOO00OO00OO00O ):#line:9
        ""#line:10
    @staticmethod #line:12
    def toPythonObjFromFile (O00OOOO0OO000OO0O ):#line:13
        ""#line:18
        with open (O00OOOO0OO000OO0O ,encoding ="utf-8")as O00O0OOOOOOO0OOO0 :#line:19
            O00OOOO0O00OOO0OO =json .load (O00O0OOOOOOO0OOO0 )#line:20
        return O00OOOO0O00OOO0OO #line:21
    @staticmethod #line:23
    def toStrByFile (OO0OO0OOOO0OO0OOO ,OO0OO0OOO0O000O0O ):#line:24
        ""#line:30
        O000O0000O0O00000 =json .dumps (OO0OO0OOO0O000O0O ,ensure_ascii =False )#line:31
        FileUtilsEx .writeAllText (OO0OO0OOOO0OO0OOO ,O000O0000O0O00000 )#line:32
