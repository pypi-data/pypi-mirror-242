import json #line:1
import random #line:2
import time #line:3
from hulk import HttpUtilsEx #line:5
class ObfuscatorUtilsEx :#line:8
    URL ="https://pyob.oxyry.com/obfuscate"#line:11
    @staticmethod #line:17
    def run (O0O000O000O0000OO ):#line:18
        ""#line:23
        OOOO00O000O0000OO ={'content-type':'application/json'}#line:26
        OOOO0O0O000O000OO =json .dumps ({"append_source":False ,"remove_docstrings":True ,"rename_nondefault_parameters":True ,"rename_default_parameters":False ,"preserve":"","source":O0O000O000O0000OO })#line:34
        O00O0OO00O00000O0 =HttpUtilsEx .post (ObfuscatorUtilsEx .URL ,OOOO00O000O0000OO ,OOOO0O0O000O000OO )#line:35
        time .sleep (random .randint (1 ,5 ))#line:36
        return O00O0OO00O00000O0 ["dest"]#line:38
