import json #line:1
import random #line:2
import time #line:3
from hulk import HttpUtilsEx #line:5
class ObfuscatorUtilsEx :#line:8
    URL ="https://pyob.oxyry.com/obfuscate"#line:11
    @staticmethod #line:17
    def run (O0000OOOO0OOO00O0 ):#line:18
        ""#line:23
        O0O0000O000O0OOOO ={'content-type':'application/json'}#line:26
        OO0OOO0OOO0OOO00O =json .dumps ({"append_source":False ,"remove_docstrings":True ,"rename_nondefault_parameters":True ,"rename_default_parameters":False ,"preserve":"","source":O0000OOOO0OOO00O0 })#line:34
        OOO000O0O00O00O00 =HttpUtilsEx .post (ObfuscatorUtilsEx .URL ,O0O0000O000O0OOOO ,OO0OOO0OOO0OOO00O )#line:35
        time .sleep (random .randint (1 ,5 ))#line:36
        return OOO000O0O00O00O00 ["dest"]#line:38
