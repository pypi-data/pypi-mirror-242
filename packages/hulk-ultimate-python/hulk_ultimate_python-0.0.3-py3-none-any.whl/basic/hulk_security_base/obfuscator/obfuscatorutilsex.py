import json #line:1
import random #line:2
import time #line:3
from basic import HttpUtilsEx #line:5
class ObfuscatorUtilsEx :#line:8
    URL ="https://pyob.oxyry.com/obfuscate"#line:11
    @staticmethod #line:17
    def run (O0O0O000O0O0OO000 ):#line:18
        ""#line:23
        OOO000OO0O00O0O0O ={'content-type':'application/json'}#line:26
        OOO0O0000000O0O00 =json .dumps ({"append_source":False ,"remove_docstrings":True ,"rename_nondefault_parameters":True ,"rename_default_parameters":False ,"preserve":"","source":O0O0O000O0O0OO000 })#line:34
        O00OOOO0OO0000OOO =HttpUtilsEx .post (ObfuscatorUtilsEx .URL ,OOO000OO0O00O0O0O ,OOO0O0000000O0O00 )#line:35
        time .sleep (random .randint (1 ,5 ))#line:36
        return O00OOOO0OO0000OOO ["dest"]#line:38
