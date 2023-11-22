class StrUtilsEx :#line:1
    ""#line:2
    def __init__ (OO000OOOO0O000O0O ):#line:4
        ""#line:5
    @staticmethod #line:7
    def contains (O0OOO00OOO0OOO00O ,O000OO00O000O0O00 ):#line:8
        ""#line:14
        for OOOOO0OO0OOO00OOO in O000OO00O000O0O00 :#line:15
            if OOOOO0OO0OOO00OOO in O0OOO00OOO0OOO00O :#line:16
                return True #line:17
        return False #line:18
    @staticmethod #line:20
    def splitWithoutEmpty (OOO0OOOO000O0OO00 ,OOOO000OOOO000000 ):#line:21
        ""#line:27
        return [OOOO000O0O0OOO0OO for OOOO000O0O0OOO0OO in OOO0OOOO000O0OO00 .split (OOOO000OOOO000000 )if OOOO000O0O0OOO0OO ]#line:28
    @staticmethod #line:30
    def replaceAdv (OOOO00O0OO00O0OOO ,O00OOO0O00000000O ,O00000OO0OOOO000O ):#line:31
        ""#line:38
        O0O000000000O0OOO =OOOO00O0OO00O0OOO #line:39
        for OO00OO000OOOOOO00 ,O0000OO0O0OOO0O00 in enumerate (O00OOO0O00000000O ):#line:40
            O0O000000000O0OOO =O0O000000000O0OOO .replace (O0000OO0O0OOO0O00 ,O00000OO0OOOO000O )#line:41
        return O0O000000000O0OOO #line:42
