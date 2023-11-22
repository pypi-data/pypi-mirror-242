import json #line:1
import random #line:2
import time #line:3
from hulk import HttpUtilsEx #line:5
class ObfuscatorUtilsEx :#line:8
    URL ="https://pyob.oxyry.com/obfuscate"#line:11
    @staticmethod #line:17
    def run (O0000OOOOO000OO00 ):#line:18
        ""#line:23
        O000000O00OO0O0OO ={'content-type':'application/json'}#line:26
        O00OO00000OO00O0O =json .dumps ({"append_source":False ,"remove_docstrings":True ,"rename_nondefault_parameters":True ,"rename_default_parameters":False ,"preserve":"","source":O0000OOOOO000OO00 })#line:34
        O00O000OOO0OO00OO =HttpUtilsEx .post (ObfuscatorUtilsEx .URL ,O000000O00OO0O0OO ,O00OO00000OO00O0O )#line:35
        time .sleep (random .randint (1 ,5 ))#line:36
        return O00O000OOO0OO00OO ["dest"]#line:38
