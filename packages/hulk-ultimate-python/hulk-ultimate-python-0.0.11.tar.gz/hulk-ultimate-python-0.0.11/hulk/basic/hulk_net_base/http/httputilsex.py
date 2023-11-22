import json #line:1
import requests #line:3
class HttpUtilsEx :#line:6
    ""#line:7
    @staticmethod #line:9
    def post (OOO0O0O0OO0OOOOO0 ,O0O0OO00OO00O00O0 ,O000OO0O0000O000O ):#line:10
        ""#line:17
        OO00O0OO0O00O0OOO =requests .request ("POST",OOO0O0O0OO0OOOOO0 ,headers =O0O0OO00OO00O00O0 ,data =O000OO0O0000O000O )#line:18
        return json .loads (OO00O0OO0O00O0OOO .text )#line:19
