class StrUtilsEx :#line:1
    ""#line:2
    def __init__ (O0OOO00O000O0O000 ):#line:4
        ""#line:5
    @staticmethod #line:7
    def contains (O0O000OO00OO0OOO0 ,O0OO0OO0O0O0OO00O ):#line:8
        ""#line:14
        for OO0O0O0O0O00OO00O in O0OO0OO0O0O0OO00O :#line:15
            if OO0O0O0O0O00OO00O in O0O000OO00OO0OOO0 :#line:16
                return True #line:17
        return False #line:18
    @staticmethod #line:20
    def splitWithoutEmpty (OO00OOO0000OOOO00 ,O00O0OOO0OOO0OOOO ):#line:21
        ""#line:27
        return [O0O0O0OO00O0O000O for O0O0O0OO00O0O000O in OO00OOO0000OOOO00 .split (O00O0OOO0OOO0OOOO )if O0O0O0OO00O0O000O ]#line:28
    @staticmethod #line:30
    def replaceAdv (O0OOO0OOO0000OOOO ,OOOOO0OOOO00O0000 ,O00O00O0O0000OOOO ):#line:31
        ""#line:38
        OOOO0OOO0OO00O000 =O0OOO0OOO0000OOOO #line:39
        for O0OOOO0OOO0OOOO0O ,O000OOO0O000O00O0 in enumerate (OOOOO0OOOO00O0000 ):#line:40
            OOOO0OOO0OO00O000 =OOOO0OOO0OO00O000 .replace (O000OOO0O000O00O0 ,O00O00O0O0000OOOO )#line:41
        return OOOO0OOO0OO00O000 #line:42
