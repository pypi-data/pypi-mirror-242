import json #line:1
import requests #line:3
class HttpUtilsEx :#line:6
    ""#line:7
    @staticmethod #line:9
    def post (O0OOOOO0O0O0OO000 ,OOO000OOO0O0OO000 ,O00OOOOOOO0OOOOO0 ):#line:10
        ""#line:17
        OO0OO0O00O00OO0OO =requests .request ("POST",O0OOOOO0O0O0OO000 ,headers =OOO000OOO0O0OO000 ,data =O00OOOOOOO0OOOOO0 )#line:18
        return json .loads (OO0OO0O00O00OO0OO .text )#line:19
