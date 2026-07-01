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

combine(np, fun(s,np,b), s, '').
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

reduce1([A,B|Rest], [C|Rest]) :-
    combine(A,B,C,_), !.
reduce1([X|Rest], [X|Rest2]) :-
    reduce1(Rest, Rest2).
reduce1([X], [X]).

parse1([C], C).
parse1(Cats, Result) :-
    reduce1(Cats, NewCats),
    length(Cats, L0),
    length(NewCats, L1),
    format('~w, ~w ~n',[L1,NewCats]),
    ( L1 < L0 ->
        % 短くなった → まだ縮約が進んでいる
        parse1(NewCats, Result)
    ;   % 長さが変わらない → これ以上は縮約できない
        Result = NewCats
    ).
/*
parse1(Cats, Result) :-
    reduce1(Cats, NewCats),
    parse1(NewCats, Result).
*/

reduce2([A,B|Rest], [C|Rest]) :-
    combine(A,B,C,_),
    !.
reduce2([X|Rest], [X|Rest2]) :-
    reduce2(Rest, Rest2).
reduce2([X], [X]).

parse2(Cats, Result) :-
    reduce2(Cats, NewCats),
    length(Cats, L0),
    length(NewCats, L1),
    ( L1 < L0 ->
        parse2(NewCats, Result)
    ;   Result = NewCats
    ).


phaseA(Cats, CatsA) :-
    log_phase('phaseA (BOX安定化)', Cats),
    parse2(Cats, CatsA),
    log_phase('phaseA result', CatsA).

phaseB(CatsA, CatsB) :-
    log_phase('phaseB (主節S化)', CatsA),
    parse1(CatsA, CatsB),
    log_phase('phaseB result', CatsB).

phaseC(CatsB, CatsC) :-
    log_phase('phaseC (副詞節弱結合)', CatsB),
    parse2(CatsB, CatsC),
    log_phase('phaseC result', CatsC).

phaseD(CatsC, Result) :-
    log_phase('phaseD (最終S化)', CatsC),
    parse1(CatsC, Result),
    log_phase('phaseD result', Result).

log_phase(Name, Cats) :-
    format("~n==== ~w ====\n", [Name]),
    format("Cats: ~w~n", [Cats]).

/*
phaseA(Cats, CatsA) :-
    parse2(Cats, CatsA).
phaseB(CatsA, CatsB) :-
    parse1(CatsA, CatsB).
phaseC(CatsB, CatsC) :-
    parse2(CatsB, CatsC).
phaseD(CatsC, Result) :-
    parse1(CatsC, Result).
*/

parse_ccg(Cats, Result) :-
    phaseA(Cats, CatsA),
    phaseB(CatsA, CatsB),
    phaseC(CatsB, CatsC),
    phaseD(CatsC, Result).


parse(Cats, Result) :-
    reduce_leftmost(Cats, NewCats),
    length(Cats, L0),
    length(NewCats, L1),
    format('~w, ~w ~n',[L1,NewCats]),
    ( L1 < L0 ->
        % 短くなった → まだ縮約が進んでいる
        parse(NewCats, Result)
    ;   % 長さが変わらない → これ以上は縮約できない
        Result = NewCats,
        writeln([Result, stop])
    ).

% 1 要素だけになったときのショートカット（任意）
parse([C], C) :-
    writeln([C,ok]).


% 左から順に 1 箇所だけ縮約を試す
reduce_leftmost([A,B|Rest], [C|Rest]) :-
    combine(A,B,C,NM),
    format("~w x ~w --> ~w     ~w~n", [A,B,C,NM]),
    !.
reduce_leftmost([X|Rest], [X|Rest2]) :-
    reduce_leftmost(Rest, Rest2).
reduce_leftmost([X], [X]).  % 末尾まで来て何もできなければそのまま

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
    en_ccg_line(11,Result).
    %en_ccg_line(23,Result).
