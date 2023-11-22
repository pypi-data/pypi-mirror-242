class StrUtilsEx :#line:1
    ""#line:2
    def __init__ (OOO0OOOO0OO00O00O ):#line:4
        ""#line:5
    @staticmethod #line:7
    def contains (O0OO0O0000O0OOOO0 ,O0O000O000000O0O0 ):#line:8
        ""#line:14
        for OO0O00O0O00O00O00 in O0O000O000000O0O0 :#line:15
            if OO0O00O0O00O00O00 in O0OO0O0000O0OOOO0 :#line:16
                return True #line:17
        return False #line:18
    @staticmethod #line:20
    def splitWithoutEmpty (OO00000OO00OOO00O ,O00O0O0OO0OO00OOO ):#line:21
        ""#line:27
        return [O0O00OO00OO0OO0OO for O0O00OO00OO0OO0OO in OO00000OO00OOO00O .split (O00O0O0OO0OO00OOO )if O0O00OO00OO0OO0OO ]#line:28
    @staticmethod #line:30
    def replaceAdv (O000O0OO0000O000O ,O0000OOO00OO0OOO0 ,OOOOO0O0O00OO0O00 ):#line:31
        ""#line:38
        O0O0OO0O0O0O000O0 =O000O0OO0000O000O #line:39
        for O0000OO000OO000O0 ,OO0O00000O0O0000O in enumerate (O0000OOO00OO0OOO0 ):#line:40
            O0O0OO0O0O0O000O0 =O0O0OO0O0O0O000O0 .replace (OO0O00000O0O0000O ,OOOOO0O0O00OO0O00 )#line:41
        return O0O0OO0O0O0O000O0 #line:42
