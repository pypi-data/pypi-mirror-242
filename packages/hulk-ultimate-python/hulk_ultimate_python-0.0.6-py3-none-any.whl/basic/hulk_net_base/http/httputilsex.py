import json #line:1
import requests #line:3
class HttpUtilsEx :#line:6
    ""#line:7
    @staticmethod #line:9
    def post (OO00O000OOOO0O000 ,OOO00OOO0O00O000O ,O0O000O00OOOOO000 ):#line:10
        ""#line:17
        OOO0O0OOOOOOOO000 =requests .request ("POST",OO00O000OOOO0O000 ,headers =OOO00OOO0O00O000O ,data =O0O000O00OOOOO000 )#line:18
        return json .loads (OOO0O0OOOOOOOO000 .text )#line:19
