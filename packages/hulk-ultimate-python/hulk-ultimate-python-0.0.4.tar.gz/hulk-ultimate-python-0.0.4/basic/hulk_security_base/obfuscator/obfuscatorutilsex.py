import json #line:1
import random #line:2
import time #line:3
from basic import HttpUtilsEx #line:5
class ObfuscatorUtilsEx :#line:8
    URL ="https://pyob.oxyry.com/obfuscate"#line:11
    @staticmethod #line:17
    def run (O00O00000O0O00000 ):#line:18
        ""#line:23
        O00OO00O00O0OOOOO ={'content-type':'application/json'}#line:26
        O0O0000OO0OO00OO0 =json .dumps ({"append_source":False ,"remove_docstrings":True ,"rename_nondefault_parameters":True ,"rename_default_parameters":False ,"preserve":"","source":O00O00000O0O00000 })#line:34
        O0OOO00OOO0OO0OO0 =HttpUtilsEx .post (ObfuscatorUtilsEx .URL ,O00OO00O00O0OOOOO ,O0O0000OO0OO00OO0 )#line:35
        time .sleep (random .randint (1 ,5 ))#line:36
        return O0OOO00OOO0OO0OO0 ["dest"]#line:38
