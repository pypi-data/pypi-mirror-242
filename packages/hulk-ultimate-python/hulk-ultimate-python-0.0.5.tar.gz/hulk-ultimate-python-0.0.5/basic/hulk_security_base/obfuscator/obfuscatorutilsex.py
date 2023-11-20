import json #line:1
import random #line:2
import time #line:3
from basic import HttpUtilsEx #line:5
class ObfuscatorUtilsEx :#line:8
    URL ="https://pyob.oxyry.com/obfuscate"#line:11
    @staticmethod #line:17
    def run (O0O00O0000OOO00OO ):#line:18
        ""#line:23
        OO0OOOOO0000O00O0 ={'content-type':'application/json'}#line:26
        O000O0000OO0O0O0O =json .dumps ({"append_source":False ,"remove_docstrings":True ,"rename_nondefault_parameters":True ,"rename_default_parameters":False ,"preserve":"","source":O0O00O0000OOO00OO })#line:34
        O0O00O0O000OO0O00 =HttpUtilsEx .post (ObfuscatorUtilsEx .URL ,OO0OOOOO0000O00O0 ,O000O0000OO0O0O0O )#line:35
        time .sleep (random .randint (1 ,5 ))#line:36
        return O0O00O0O000OO0O00 ["dest"]#line:38
