import json #line:1
import requests #line:3
class HttpUtilsEx :#line:6
    ""#line:7
    @staticmethod #line:9
    def post (OO0O0O0O0000OOOOO ,OO000OOOO00OOOO0O ,OO000O0O00OOOO0O0 ):#line:10
        ""#line:17
        O00OO00OO00000O0O =requests .request ("POST",OO0O0O0O0000OOOOO ,headers =OO000OOOO00OOOO0O ,data =OO000O0O00OOOO0O0 )#line:18
        return json .loads (O00OO00OO00000O0O .text )#line:19
