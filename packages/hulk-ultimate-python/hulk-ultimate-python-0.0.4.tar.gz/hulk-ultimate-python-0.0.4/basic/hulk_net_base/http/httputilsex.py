import json #line:1
import requests #line:3
class HttpUtilsEx :#line:6
    ""#line:7
    @staticmethod #line:9
    def post (O0OO000OOOO000OOO ,O00OO000OOO000O0O ,O000OOO0O0OOOO0OO ):#line:10
        ""#line:17
        OO00OOO0O0OOO0O00 =requests .request ("POST",O0OO000OOOO000OOO ,headers =O00OO000OOO000O0O ,data =O000OOO0O0OOOO0OO )#line:18
        return json .loads (OO00OOO0O0OOO0O00 .text )#line:19
