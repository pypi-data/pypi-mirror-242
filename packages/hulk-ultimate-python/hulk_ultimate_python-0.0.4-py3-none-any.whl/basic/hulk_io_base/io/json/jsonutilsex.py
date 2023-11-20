import json #line:1
from basic import FileUtilsEx #line:3
class JsonUtilsEx :#line:6
    ""#line:7
    def __init__ (OO00000OOOO00O0O0 ):#line:9
        ""#line:10
    @staticmethod #line:12
    def toPythonObjFromFile (O00OOOOO00000OO0O ):#line:13
        ""#line:18
        with open (O00OOOOO00000OO0O ,encoding ="utf-8")as O0OO00000OO0000OO :#line:19
            O00O0OOO00O00OO00 =json .load (O0OO00000OO0000OO )#line:20
        return O00O0OOO00O00OO00 #line:21
    @staticmethod #line:23
    def toStrByFile (OO0OOO0OOOO00O0O0 ,O0000000O0O0O0O0O ):#line:24
        ""#line:30
        O00O00O0O0O0OOO00 =json .dumps (O0000000O0O0O0O0O ,ensure_ascii =False )#line:31
        FileUtilsEx .writeAllText (OO0OOO0OOOO00O0O0 ,O00O00O0O0O0OOO00 )#line:32
