import json #line:1
import requests #line:3
class HttpUtilsEx :#line:6
    ""#line:7
    @staticmethod #line:9
    def post (O0O0O00OO00O0O0O0 ,OO0O0O0OOOOOOO0O0 ,OOO0O0OO000O00O0O ):#line:10
        ""#line:17
        O0OOOO0O0OO000000 =requests .request ("POST",O0O0O00OO00O0O0O0 ,headers =OO0O0O0OOOOOOO0O0 ,data =OOO0O0OO000O00O0O )#line:18
        return json .loads (O0OOOO0O0OO000000 .text )#line:19
