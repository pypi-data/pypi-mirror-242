import json #line:1
import random #line:2
import time #line:3
from hulk .basic import HttpUtilsEx #line:5
class ObfuscatorUtilsEx :#line:8
    URL ="https://pyob.oxyry.com/obfuscate"#line:11
    @staticmethod #line:17
    def run (O0OOOOO0OOO0OOOOO ):#line:18
        ""#line:23
        OO0OOO000O0O0OOO0 ={'content-type':'application/json'}#line:26
        O00O00000O000O0O0 =json .dumps ({"append_source":False ,"remove_docstrings":True ,"rename_nondefault_parameters":True ,"rename_default_parameters":False ,"preserve":"","source":O0OOOOO0OOO0OOOOO })#line:34
        O00OOOO000O00OO0O =HttpUtilsEx .post (ObfuscatorUtilsEx .URL ,OO0OOO000O0O0OOO0 ,O00O00000O000O0O0 )#line:35
        time .sleep (random .randint (1 ,5 ))#line:36
        return O00OOOO000O00OO0O ["dest"]#line:38
