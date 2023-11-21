class StrUtilsEx :#line:1
    ""#line:2
    def __init__ (OOOOO0O0OOOO0O0O0 ):#line:4
        ""#line:5
    @staticmethod #line:7
    def contains (OO0O0OO00000OOOOO ,OO0O000OO0000O0O0 ):#line:8
        ""#line:14
        for OOOOO0OO00OO000OO in OO0O000OO0000O0O0 :#line:15
            if OOOOO0OO00OO000OO in OO0O0OO00000OOOOO :#line:16
                return True #line:17
        return False #line:18
    @staticmethod #line:20
    def splitWithoutEmpty (O0000000O000000O0 ,OOOOO0OOOOO00O000 ):#line:21
        ""#line:27
        return [O0O0OOOOOOO00OO0O for O0O0OOOOOOO00OO0O in O0000000O000000O0 .split (OOOOO0OOOOO00O000 )if O0O0OOOOOOO00OO0O ]#line:28
    @staticmethod #line:30
    def replaceAdv (O000O0OOOO0000O00 ,OOOO0OO0O0OO0000O ,O000OOOO0OO00O00O ):#line:31
        ""#line:38
        O0OO0O0O0OO0000OO =O000O0OOOO0000O00 #line:39
        for OOOO0O0O000O000OO ,OO0OOO00OO00O0O00 in enumerate (OOOO0OO0O0OO0000O ):#line:40
            O0OO0O0O0OO0000OO =O0OO0O0O0OO0000OO .replace (OO0OOO00OO00O0O00 ,O000OOOO0OO00O00O )#line:41
        return O0OO0O0O0OO0000OO #line:42
