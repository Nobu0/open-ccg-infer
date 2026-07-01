:- use_module(tbl_inf).

cat("DT",np).
cat("NNP",np).
cat("NN",np).
cat("NNS",np).
cat("NNPS",np).
cat("IN",fun(np,np,f)).
cat("TO",fun(s,s,f)).
cat("LS",np).
cat("JJ",np).
cat("CD",np).
cat(",",np).
cat(".",np).
cat(";",np).
cat("EX",np).
cat("PDT",np).
cat("PRP",np).
cat("-LRB-",np).
cat("-RRB-",np).

cat("RB",fun(s,s,f)).
cat("RBR",fun(s,s,f)).
cat("RBS",fun(s,s,f)).
cat("WRB",fun(s,s,f)).   % when, where → 副詞節
cat("WDT", fun(s/np, np, f)).
cat("WP", fun(s/np, np, f)).
cat("WP$", fun(s/np, np, f)).
cat("CC",fun(fun(np,np,b), np, f)).
%cat("MD",fun(s, fun(s,np,b), b)).
cat("MD", fun(s, fun(s,np,b), b)).   % shall
%cat("VB",fun(fun(s,np,b),np,f)).
cat("VB", fun(fun(s,np,b), np, f)). % revise
cat("VBP", fun(fun(s,np,b), np, f)).
cat("VBZ", fun(fun(s,np,b), np, f)).
cat("VBD", fun(fun(s,np,b), np, f)).
cat("VBN", fun(np,np,f)). % 過去分詞の名詞修飾
cat("VBG", fun(np,np,f)). % 動名詞の名詞修飾
cat(X,_):- writeln(X),err.

/*
% 副詞節以外の pp は結合しない
combine(np, pp, _) :- fail.
combine(pp, np, _) :- fail.
combine(pp, pp, _) :- fail.
combine(fun(X, Y, f), Y, X, 'Forward Application').
combine(Y, fun(X, Y, b), X, 'Backward Application').
combine(np, fun(s,np,b), s, 'Subject-Verb').
combine(fun(s,np,b), np, s, 'Verb-Object').
% S に右側から副詞節が付く（典型的な when, due to, or any other circumstances）
combine(s, fun(s,s,f), s, 'S-Adv-Right').
% 副詞節が前置される場合（when necessary, S ...）
combine(fun(s,s,f), s, s, 'S-Adv-Left').
% VP に副詞節が付いても VP のまま（shall revise NP when necessary）
combine(fun(s,np,b), fun(s,s,f), fun(s,np,b), 'VP-Adv').

combine(np, fun(s,np,f), s, '').
%combine(s, fun(s,s,f), s, '').
%combine(fun(s,s,f), s, s, '').
combine(fun(s,np,f), fun(s,s,f), fun(s,np,f), '').
combine(np, fun(fun(s,np,b),np,f), fun(s,np,b), '').
combine(fun(s,np,b), fun(s,np,b), fun(s,np,b), '').
%combine(fun(s,np,b), fun(s,s,f), fun(s,np,b), '').
combine(s, fun(s,np,b), s, '').
combine(np, fun(fun(s,np,b),np,f), fun(s,np,b), '').
combine(fun(s,np,b), fun(s,np,b), fun(s,np,b), '').
combine(fun(s,np,b), fun(s,s,f), s, '').
%combine(np, fun(s,s,f), np, '').
combine(fun(fun(s,np,b),np,f), fun(s,np,b), fun(s,np,b), '').
combine(np, s, s, '').
%combine(np, np, np, '名詞句連接/弱い').
combine(s, s, s, '弱い結合').
combine(np, fun(s,np,b), s, '').
combine(fun(s,fun(s,np,b),b), fun(s,np,b), s, '').
combine(s, np, s, '').
% これは構造を壊しやすいので、優先度を下げるか削除候補
combine(np, fun(s,s,f), np, '').
combine(fun(s,s,f), s, s, '').
*/

% ==============================
% 1. 危険な PP 弱結合は封印
% ==============================
combine(np, pp, _, _) :- fail.
combine(pp, np, _, _) :- fail.
combine(pp, pp, _, _) :- fail.

% ==============================
% 2. 正統 CCG 規則（チャネル: main）
% ==============================
% Forward / Backward Application
combine(fun(X, Y, f), Y, X, 'Forward Application', channel(main)).
combine(Y, fun(X, Y, b), X, 'Backward Application', channel(main)).

% 主節：NP + VP → S / VP + NP → S
combine(np, fun(s,np,b), s, 'Subject-Verb', channel(main)).
combine(fun(s,np,b), np, s, 'Verb-Object', channel(main)).

% S に右側から副詞節が付く
combine(s, fun(s,s,f), s, 'S-Adv-Right', channel(adjunct)).
% 副詞節が前置される場合
combine(fun(s,s,f), s, s, 'S-Adv-Left', channel(adjunct)).
% VP に副詞節が付いても VP のまま
combine(fun(s,np,b), fun(s,s,f), fun(s,np,b), 'VP-Adv', channel(adjunct)).

% ==============================
% 3. 既存の弱結合系（チャネル振り分け）
% ==============================

% NP + fun(s,np,f) → S（助動詞＋VP など）
combine(np, fun(s,np,f), s, '', channel(main)).

% fun(s,np,f) + S/S → fun(s,np,f)（VP に副詞節）
combine(fun(s,np,f), fun(s,s,f), fun(s,np,f), '', channel(adjunct)).

% VP 拡張：((S\NP)/NP) + NP → (S\NP)
combine(np, fun(fun(s,np,b),np,f), fun(s,np,b), '', channel(main)).
combine(fun(fun(s,np,b),np,f), fun(s,np,b), fun(s,np,b), '', channel(main)).

% VP 同士の弱結合（ほぼ維持）
combine(fun(s,np,b), fun(s,np,b), fun(s,np,b), '', channel(main)).

% S + VP → S
combine(s, fun(s,np,b), s, '', channel(main)).

% VP + S/S → S（やや強いが main 側で扱う）
combine(fun(s,np,b), fun(s,s,f), s, '', channel(main)).

% NP + S → S（主語が後置されるような特殊構造）
combine(np, s, s, '', channel(main)).

% S + S → S（弱い結合）
combine(s, s, s, '弱い結合', channel(main)).

% NP + VP → S（ラベル違いだが保持）
combine(np, fun(s,np,b), s, '', channel(main)).

% S + VP（助動詞句）→ S
combine(fun(s,fun(s,np,b),b), fun(s,np,b), s, '', channel(main)).

% S + NP → S（後置主語など）
combine(s, np, s, '', channel(main)).

% NP + S/S → NP（構造を壊しやすいが一旦 adjunct に）
combine(np, fun(s,s,f), np, '', channel(adjunct)).

% S/S + S → S（既存のものを adjunct に）
combine(fun(s,s,f), s, s, '', channel(adjunct)).

% 名詞修飾を NP に吸収（box チャネル）
combine(fun(np,np,f), np, np, 'N-Adj-Right', channel(box)).
combine(np, fun(np,np,f), np, 'N-Adj-Left',  channel(box)).

% 関係節 s/np を NP に吸収（which / that 節など）
combine(np, s/np, np, 'RelClause-NP', channel(box)).


% 汎用安全縮約
parse_safe(Reduce, Cats, Result) :-
    call(Reduce, Cats, NewCats),
    length(Cats, L0),
    length(NewCats, L1),
    ( L1 < L0 ->
        parse_safe(Reduce, NewCats, Result)
    ;   Result = Cats ).

% A: BOX / 弱結合（VPを触らない）
reduceA([A,B|Rest], [C|Rest]) :-
    combine(A,B,C,_,channel(box)), !.
reduceA([X|Rest], [X|Rest2]) :-
    reduceA(Rest, Rest2).
reduceA([X], [X]).

% B: 主節 S 化
reduceB([A,B|Rest], [C|Rest]) :-
    combine(A,B,C,_,channel(main)), !.
reduceB([X|Rest], [X|Rest2]) :-
    reduceB(Rest, Rest2).
reduceB([X], [X]).

% C: 副詞節弱結合
reduceC([A,B|Rest], [C|Rest]) :-
    combine(A,B,C,_,channel(adjunct)), !.
reduceC([X|Rest], [X|Rest2]) :-
    reduceC(Rest, Rest2).
reduceC([X], [X]).

% D: 最終 S 化（main をもう一度）
reduceD([A,B|Rest], [C|Rest]) :-
    combine(A,B,C,_,channel(main)), !.
reduceD([X|Rest], [X|Rest2]) :-
    reduceD(Rest, Rest2).
reduceD([X], [X]).

% 統合パーサ
parse_ccg(Cats, Result) :-
    parse_safe(reduceA, Cats, CatsA),
    parse_safe(reduceB, CatsA, CatsB),
    parse_safe(reduceC, CatsB, CatsC),
    parse_safe(reduceD, CatsC, Result).

parse([C], C):- writeln([C,ok]).

parse(Cats, Result) :-
    reduce_leftmost(Cats, NewCats),
    length(Cats, L0),
    length(NewCats, L1),
    format('~w, ~w ~n',[L1,NewCats]),
    ( L1 < L0 ->
        parse(NewCats, Result)
    ;   % 長さが変わらない → これ以上縮約できない
        Result = NewCats,
        writeln([Result, stop])
    ).

/*

parse(Cats, Result) :-
    reduce_leftmost(Cats, NewCats),
    length(NewCats,LN),
    format('~w, ~w ~n',[LN,NewCats]),
    parse(NewCats, Result).
*/

reduce_leftmost([A,B|Rest], [C|Rest]) :-
    combine(A,B,C,NM),
    format("~w x ~w --> ~w     ~w~n", [A,B,C,NM]).%,!.

reduce_leftmost([X|Rest], [X|Rest2]) :-
    reduce_leftmost(Rest, Rest2).

en_chunk_cat([], _, []).
en_chunk_cat([[ID|X]|T], [[305,ST,ED,BX]|TB], TK) :-
    % VP は BOX 化しない
    en_chunk_cat([[ID|X]|T], TB, TK).
en_chunk_cat([[ID|X]|T], [[CL,ID,ED,BX]|TB], [Cat|TK]) :-
    box_cat(CL, Cat),
    writeln([box,'->',ID,ED,CL,Cat,BX]),
    LN is 1 + ED - ID,
    length(NX,LN),
    append(NX,TX,[[ID|X]|T]),
    %writeln([NX,TX]),
    en_chunk_cat(TX, TB, TK).
en_chunk_cat([[ID|X]|T], [[CL,ST,ED|_]|TB], TK) :-
    ID > ST,
    ID > ED,
    %writeln([skip,CL,ID,X,ST,ED]),
    en_chunk_cat([[ID|X]|T], TB, TK).
en_chunk_cat([[ID,_,P|W]|T], CLX, [Cat|TK]) :-
    %writeln([cat1,ID,P,W,Cat]),
    cat(P, Cat),
    writeln([cat2,ID,P,W,Cat]),
    en_chunk_cat(T, CLX, TK).


box_cat(ClassId, np) :- ClassId >= 300, ClassId < 400.
box_cat(ClassId, pp) :- ClassId >= 400, ClassId < 500.
%box_cat(ClassId, s/np) :- ClassId >= 500, ClassId < 600.
% CLAUSE_WH（when necessary, due to ...）
box_cat(ClassId, fun(s,s,f)) :- ClassId >= 500, ClassId < 550.
% CLAUSE_WHICH（or any other circumstances）
box_cat(ClassId, fun(s,s,f)) :- ClassId >= 550, ClassId < 600.

en_ccg_line(NO,Result) :-
    findall([A,NO,C,D],pos_tbl(A,NO,C,D),LS),
    writeln(LS),
    nth0(0,LS,[HD|_]),
    last(LS,[TA|_]),
    writeln([HD,TA]),
    findall([A,B,C,D],(box_tbl(A,B,C,D),B>=HD,C=<TA),LSB),
    writeln(LSB),
    en_chunk_cat(LS, LSB, Cats),!,
    writeln(Cats),
    parse_ccg(Cats, Result).

main:-
    %en_ccg_line(11,Result),
    en_ccg_line(23,Result),
    writeln(Result).
