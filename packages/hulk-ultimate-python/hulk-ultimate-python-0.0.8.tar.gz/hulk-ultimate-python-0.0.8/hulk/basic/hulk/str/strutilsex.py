class StrUtilsEx :#line:1
    ""#line:2
    def __init__ (O00000O00OO0O0OO0 ):#line:4
        ""#line:5
    @staticmethod #line:7
    def contains (O0OO00000O000OOO0 ,O0O00OOOO0OO00000 ):#line:8
        ""#line:14
        for O0OO00O00OOOOO0O0 in O0O00OOOO0OO00000 :#line:15
            if O0OO00O00OOOOO0O0 in O0OO00000O000OOO0 :#line:16
                return True #line:17
        return False #line:18
    @staticmethod #line:20
    def splitWithoutEmpty (OOOO00O0O000O0OO0 ,O0O0OOO0O0000OOO0 ):#line:21
        ""#line:27
        return [O0OOOOO0000000OO0 for O0OOOOO0000000OO0 in OOOO00O0O000O0OO0 .split (O0O0OOO0O0000OOO0 )if O0OOOOO0000000OO0 ]#line:28
    @staticmethod #line:30
    def replaceAdv (OOO0000OO000O0OO0 ,OOO0OOOOO0OO00O0O ,OOOO0OOO0000O0OOO ):#line:31
        ""#line:38
        OO0OOO0OO000OOO0O =OOO0000OO000O0OO0 #line:39
        for O00000OO0000O0OOO ,O0OOO0OO0OO0O0000 in enumerate (OOO0OOOOO0OO00O0O ):#line:40
            OO0OOO0OO000OOO0O =OO0OOO0OO000OOO0O .replace (O0OOO0OO0OO0O0000 ,OOOO0OOO0000O0OOO )#line:41
        return OO0OOO0OO000OOO0O #line:42
