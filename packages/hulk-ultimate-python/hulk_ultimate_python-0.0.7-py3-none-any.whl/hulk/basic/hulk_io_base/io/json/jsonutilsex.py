import json #line:1
from hulk .basic import FileUtilsEx #line:3
class JsonUtilsEx :#line:6
    ""#line:7
    def __init__ (OOOOO0OOO0O0000OO ):#line:9
        ""#line:10
    @staticmethod #line:12
    def toPythonObjFromFile (OO0000O000O00OOOO ):#line:13
        ""#line:18
        with open (OO0000O000O00OOOO ,encoding ="utf-8")as O000OO0OO000O0O0O :#line:19
            O000000OOOOOOO000 =json .load (O000OO0OO000O0O0O )#line:20
        return O000000OOOOOOO000 #line:21
    @staticmethod #line:23
    def toStrByFile (OOOOO0000000O0OOO ,O0OOOO00OOOOO0OO0 ):#line:24
        ""#line:30
        O0OO000O00OOO0000 =json .dumps (O0OOOO00OOOOO0OO0 ,ensure_ascii =False )#line:31
        FileUtilsEx .writeAllText (OOOOO0000000O0OOO ,O0OO000O00OOO0000 )#line:32
