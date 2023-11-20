import json #line:1
from basic import FileUtilsEx #line:3
class JsonUtilsEx :#line:6
    ""#line:7
    def __init__ (OO0OOO0OO0O000OOO ):#line:9
        ""#line:10
    @staticmethod #line:12
    def toPythonObjFromFile (OO0O00O00O00000O0 ):#line:13
        ""#line:18
        with open (OO0O00O00O00000O0 ,encoding ="utf-8")as O0OOO00000O00O000 :#line:19
            O00OO000O00O00OOO =json .load (O0OOO00000O00O000 )#line:20
        return O00OO000O00O00OOO #line:21
    @staticmethod #line:23
    def toStrByFile (OOOOO00OOO000OOO0 ,OOO0O0OO0000OO0O0 ):#line:24
        ""#line:30
        OOOOOOO0000OOO0OO =json .dumps (OOO0O0OO0000OO0O0 ,ensure_ascii =False )#line:31
        FileUtilsEx .writeAllText (OOOOO00OOO000OOO0 ,OOOOOOO0000OOO0OO )#line:32
