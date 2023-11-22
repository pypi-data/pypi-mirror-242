import json #line:1
import requests #line:3
class HttpUtilsEx :#line:6
    ""#line:7
    @staticmethod #line:9
    def post (O0OO00OO00O00OO00 ,O0OO0O0OOOOOO000O ,O000OO0O0O0OO0000 ):#line:10
        ""#line:17
        OO0OOO00OO00OO000 =requests .request ("POST",O0OO00OO00O00OO00 ,headers =O0OO0O0OOOOOO000O ,data =O000OO0O0O0OO0000 )#line:18
        return json .loads (OO0OOO00OO00OO000 .text )#line:19
