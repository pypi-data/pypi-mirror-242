import json #line:1
from hulk import FileUtilsEx #line:3
class JsonUtilsEx :#line:6
    ""#line:7
    def __init__ (O0O00O0O00O00OO00 ):#line:9
        ""#line:10
    @staticmethod #line:12
    def toPythonObjFromFile (OO000O00OO000OOO0 ):#line:13
        ""#line:18
        with open (OO000O00OO000OOO0 ,encoding ="utf-8")as OO00O0O0000OOOO00 :#line:19
            OO00O0OOO0OOO000O =json .load (OO00O0O0000OOOO00 )#line:20
        return OO00O0OOO0OOO000O #line:21
    @staticmethod #line:23
    def toStrByFile (O0O000OO0OOO0OOOO ,OO00O000O0O0000OO ):#line:24
        ""#line:30
        OOO0OOOOO00000O00 =json .dumps (OO00O000O0O0000OO ,ensure_ascii =False )#line:31
        FileUtilsEx .writeAllText (O0O000OO0OOO0OOOO ,OOO0OOOOO00000O00 )#line:32
