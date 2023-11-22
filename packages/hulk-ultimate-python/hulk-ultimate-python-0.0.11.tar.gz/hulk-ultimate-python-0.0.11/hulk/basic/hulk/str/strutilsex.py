class StrUtilsEx :#line:1
    ""#line:2
    def __init__ (OO0O0OOO000OO0O00 ):#line:4
        ""#line:5
    @staticmethod #line:7
    def contains (O000O0O0O0OO0000O ,O000OOO0O0OOOO000 ):#line:8
        ""#line:14
        for O000O000O00OO0OO0 in O000OOO0O0OOOO000 :#line:15
            if O000O000O00OO0OO0 in O000O0O0O0OO0000O :#line:16
                return True #line:17
        return False #line:18
    @staticmethod #line:20
    def splitWithoutEmpty (OO00000O0O00OO0OO ,OOO0000O000000O00 ):#line:21
        ""#line:27
        return [O000000OO0O000OOO for O000000OO0O000OOO in OO00000O0O00OO0OO .split (OOO0000O000000O00 )if O000000OO0O000OOO ]#line:28
    @staticmethod #line:30
    def replaceAdv (O0OOOO000OO0O00O0 ,O00OOOO0O000000OO ,OO00OO00OOO00OO0O ):#line:31
        ""#line:38
        OOO00000OO0000OO0 =O0OOOO000OO0O00O0 #line:39
        for O0OOO0O000OOO0O00 ,O000OOOO000O0O000 in enumerate (O00OOOO0O000000OO ):#line:40
            OOO00000OO0000OO0 =OOO00000OO0000OO0 .replace (O000OOOO000O0O000 ,OO00OO00OOO00OO0O )#line:41
        return OOO00000OO0000OO0 #line:42
