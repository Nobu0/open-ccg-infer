% カテゴリ及び候補、[発火候補右、左],[発火先](制約条件)
cat(s,                     [l,r], [fb]).
cat(np,                    [l,r], [fb]).
%cat(n,                     [],    []).
cat(fun(s,np,b),           [l,r], [fb]). % 主語待ちの述語(VP) S\NP
cat(fun(s,np,f),           [r],   [fb]). % 文全体を修飾する名詞句 S/NP
cat(fun(s,fun(s,np,b),b),  [l],   []).   % 副詞節として定義 S\(S\NP)
cat(fun(s,s,f),            [l,r], []).   % 文全体を修飾する副詞 S/S
cat(fun(fun(s,np,b),np,f), [l,r], []).   % 動詞(V)として定義 (S\NP)/NP


% 発火条件 ------------------------------
combine(fun(X, Y, f), Y, X, 'Forward Application').
combine(Y, fun(X, Y, b), X, 'Backward Application').
combine(np,                    s,                     s, '').
combine(np,                    np,                    np, '名詞句連接/弱い').
combine(s,                     s,                     s, '弱い結合').
combine(np,                    fun(s,s,f),            np, '').
combine(np,                    fun(s,np,f),           s, '').
combine(s,                     fun(s,s,f),            s, '').
combine(s,                     fun(s,np,b),           s, 'BA').
combine(np,                    fun(s,np,b),           s, 'BA').
combine(np,                    fun(fun(s,np,b),np,f), fun(s,np,b), '').
combine(fun(s,np,b),           fun(s,s,f),            fun(s,np,b), '').
combine(fun(s,np,b),           fun(s,s,f),            s, '').
combine(fun(s,np,b),           fun(s,np,b),           fun(s,np,b), '').
combine(fun(s,np,f),           np,                    s, 'FA').
combine(fun(s,np,f),           fun(s,s,f),            fun(s,np,f), '').
combine(fun(s,fun(s,np,b),b),  fun(s,np,b),           s, '').
combine(fun(s,s,f),            s,                     s, 'FA').
combine(fun(fun(s,np,b),np,f), fun(s,np,b),           fun(s,np,b), '').

/* 

状態遷移表サンプル、副詞節:S\(S\NP)、動詞:(S\NP)/NP
この表の見方は、横の１行目がタイトル（左）で、縦の１列目がタイトル（右）を表す。
S\NP：主語（NP）を左から受け取ると文（S）になる述語（VP）。
N は NP に昇格してから使われる(type lifting)のでこの表では削除されている。
=============================================================================
                S      NP      |  S\NP     S/NP     S\(S\NP)  S/S   (S\NP)/NP
S               [S]    [S]     |  [S]      -        -         [S]   -   
NP              -      [NP]    |  [S]      -        [S]       -     -
-----------------------------------------------------------------------------
S\NP            [S]    [S]     |  [S\NP]   -        [S]       -     [S\NP]
S/NP            -      [S]     |  -        -        -         -     -
(S\NP)/NP       -      [S\NP]  |  -        -        -         -     -
S/S             [S]    [NP]    |  [S\NP]   [S/NP]   -         -     -

*/