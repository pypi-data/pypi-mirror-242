import json #line:1
import random #line:2
import time #line:3
from basic import HttpUtilsEx #line:5
class ObfuscatorUtilsEx :#line:8
    URL ="https://pyob.oxyry.com/obfuscate"#line:11
    @staticmethod #line:17
    def run (O0OO0O0OO000OOOOO ):#line:18
        ""#line:23
        OOO00OO0O00OO0O00 ={'content-type':'application/json'}#line:26
        O0OO0O0OO00OOO00O =json .dumps ({"append_source":False ,"remove_docstrings":True ,"rename_nondefault_parameters":True ,"rename_default_parameters":False ,"preserve":"","source":O0OO0O0OO000OOOOO })#line:34
        O0O000O00OOOOOOO0 =HttpUtilsEx .post (ObfuscatorUtilsEx .URL ,OOO00OO0O00OO0O00 ,O0OO0O0OO00OOO00O )#line:35
        time .sleep (random .randint (1 ,5 ))#line:36
        return O0O000O00OOOOOOO0 ["dest"]#line:38
