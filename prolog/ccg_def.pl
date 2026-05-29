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

========================================================
サブ表1：リフティング専用表（NP → 高階カテゴリ）
例：

元カテゴリ	リフティング後	方向性	用途
NP	S/(S\NP)	/	主語の持ち上げ
NP	S\ (S/NP)	\	目的語の持ち上げ


サブ表2：文修飾カテゴリ表（S/S, S\S）
例：

修飾語	カテゴリ	説明
quickly	S/S	文修飾副詞
probably	S/S	モダリティ
because	(S\S)/S	従属節導入
although	(S\S)/S	逆接節

サブ表3：高階カテゴリの合成表（関数の関数）
例：

左	右	結果	規則
S/(S\NP)	S\NP	S	関数適用
(S\S)/S	S	S\S	従属節の構築
S/(S/NP)	S/NP	S	高階関数の適用

============================================
第一表は「句の射」
第二表は「文の射」
第三表は「射の射（高階関数）」


Steedman の slash 記法の哲学を自分で理解した説明
X/Y  Y  => X
Y   X\Y => X

X が視点（返り値）で、関数そのもの。
Y が引数。
引数が右にあるときは /、左にあるときは \ を使う。
関数の答えはXになる。

*/