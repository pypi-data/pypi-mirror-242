import json #line:1
import requests #line:3
class HttpUtilsEx :#line:6
    ""#line:7
    @staticmethod #line:9
    def post (OOOOO00O0O00O0000 ,O0O0O0O00OO000O00 ,OO00O000OOOO0OO00 ):#line:10
        ""#line:17
        OO00OOO00OO00O000 =requests .request ("POST",OOOOO00O0O00O0000 ,headers =O0O0O0O00OO000O00 ,data =OO00O000OOOO0OO00 )#line:18
        return json .loads (OO00OOO00OO00O000 .text )#line:19
