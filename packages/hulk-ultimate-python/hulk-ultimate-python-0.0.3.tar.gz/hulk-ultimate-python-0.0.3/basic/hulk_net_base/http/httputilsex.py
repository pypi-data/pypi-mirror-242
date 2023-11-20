import json #line:1
import requests #line:3
class HttpUtilsEx :#line:6
    ""#line:7
    @staticmethod #line:9
    def post (O0OO00O0O0OOO0OO0 ,OOO0O0O0OO0O00OOO ,OOO0OO00000O0OO00 ):#line:10
        ""#line:17
        O0O0O0000O000OO00 =requests .request ("POST",O0OO00O0O0OOO0OO0 ,headers =OOO0O0O0OO0O00OOO ,data =OOO0OO00000O0OO00 )#line:18
        return json .loads (O0O0O0000O000OO00 .text )#line:19
