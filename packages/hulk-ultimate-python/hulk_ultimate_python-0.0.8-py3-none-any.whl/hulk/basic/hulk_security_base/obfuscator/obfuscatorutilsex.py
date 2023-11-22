import json #line:1
import random #line:2
import time #line:3
from hulk .basic import HttpUtilsEx #line:5
class ObfuscatorUtilsEx :#line:8
    URL ="https://pyob.oxyry.com/obfuscate"#line:11
    @staticmethod #line:17
    def run (O000OO000OOO0O0O0 ):#line:18
        ""#line:23
        O00O000OO0OOO0O00 ={'content-type':'application/json'}#line:26
        OO00OOO0O0000OO00 =json .dumps ({"append_source":False ,"remove_docstrings":True ,"rename_nondefault_parameters":True ,"rename_default_parameters":False ,"preserve":"","source":O000OO000OOO0O0O0 })#line:34
        OO00OO00O0000OOOO =HttpUtilsEx .post (ObfuscatorUtilsEx .URL ,O00O000OO0OOO0O00 ,OO00OOO0O0000OO00 )#line:35
        time .sleep (random .randint (1 ,5 ))#line:36
        return OO00OO00O0000OOOO ["dest"]#line:38
