class StrUtilsEx :#line:1
    ""#line:2
    def __init__ (O0O00OO0OO0O00O0O ):#line:4
        ""#line:5
    @staticmethod #line:7
    def contains (OO00OOO00000O000O ,O0OO0O0OO00O00OOO ):#line:8
        ""#line:14
        for O00O000000O0OOO00 in O0OO0O0OO00O00OOO :#line:15
            if O00O000000O0OOO00 in OO00OOO00000O000O :#line:16
                return True #line:17
        return False #line:18
    @staticmethod #line:20
    def splitWithoutEmpty (OO00OOOO00O0OOOOO ,OO0OOOO00O0O0OO0O ):#line:21
        ""#line:27
        return [O0O0OOO00OO00OOOO for O0O0OOO00OO00OOOO in OO00OOOO00O0OOOOO .split (OO0OOOO00O0O0OO0O )if O0O0OOO00OO00OOOO ]#line:28
    @staticmethod #line:30
    def replaceAdv (O00OOO00OO000OOOO ,OOOO00000OOO0O00O ,O0O0O00OOO00O0OOO ):#line:31
        ""#line:38
        OO0OO00O0O00000OO =O00OOO00OO000OOOO #line:39
        for OOOO000OOO0OOO0OO ,OO000OOOO00O0O0OO in enumerate (OOOO00000OOO0O00O ):#line:40
            OO0OO00O0O00000OO =OO0OO00O0O00000OO .replace (OO000OOOO00O0O0OO ,O0O0O00OOO00O0OOO )#line:41
        return OO0OO00O0O00000OO #line:42
