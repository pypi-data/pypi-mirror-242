import json #line:1
import requests #line:3
class HttpUtilsEx :#line:6
    ""#line:7
    @staticmethod #line:9
    def post (OO0OOO0O0O0O00O00 ,O00OOO0OO00OO0OOO ,O00OO00O0OO0OO0OO ):#line:10
        ""#line:17
        OO000000O00O00O00 =requests .request ("POST",OO0OOO0O0O0O00O00 ,headers =O00OOO0OO00OO0OOO ,data =O00OO00O0OO0OO0OO )#line:18
        return json .loads (OO000000O00O00O00 .text )#line:19
