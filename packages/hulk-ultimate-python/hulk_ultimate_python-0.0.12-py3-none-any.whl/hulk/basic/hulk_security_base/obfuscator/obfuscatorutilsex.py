import json #line:1
import random #line:2
import time #line:3
from hulk import HttpUtilsEx #line:5
class ObfuscatorUtilsEx :#line:8
    URL ="https://pyob.oxyry.com/obfuscate"#line:11
    @staticmethod #line:17
    def run (OOO0000OOOOOO0OO0 ):#line:18
        ""#line:23
        OO0O00OOOOO0O0OOO ={'content-type':'application/json'}#line:26
        O0O00O0OOO00OO000 =json .dumps ({"append_source":False ,"remove_docstrings":True ,"rename_nondefault_parameters":True ,"rename_default_parameters":False ,"preserve":"","source":OOO0000OOOOOO0OO0 })#line:34
        OOOOO0000O00OOOO0 =HttpUtilsEx .post (ObfuscatorUtilsEx .URL ,OO0O00OOOOO0O0OOO ,O0O00O0OOO00OO000 )#line:35
        time .sleep (random .randint (1 ,5 ))#line:36
        return OOOOO0000O00OOOO0 ["dest"]#line:38
