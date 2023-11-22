import json #line:1
from hulk import FileUtilsEx #line:3
class JsonUtilsEx :#line:6
    ""#line:7
    def __init__ (OO0000OO00OOO00OO ):#line:9
        ""#line:10
    @staticmethod #line:12
    def toPythonObjFromFile (OO0000O0O0000O0O0 ):#line:13
        ""#line:18
        with open (OO0000O0O0000O0O0 ,encoding ="utf-8")as O0OOOOO000OO000O0 :#line:19
            O00O0O0OO0OO0O00O =json .load (O0OOOOO000OO000O0 )#line:20
        return O00O0O0OO0OO0O00O #line:21
    @staticmethod #line:23
    def toStrByFile (OO0000OO0000OO0O0 ,O0OO0O0000000O000 ):#line:24
        ""#line:30
        OO000OO000O0O000O =json .dumps (O0OO0O0000000O000 ,ensure_ascii =False )#line:31
        FileUtilsEx .writeAllText (OO0000OO0000OO0O0 ,OO000OO000O0O000O )#line:32
