
%en:wrd([1,242,11,[0,0,0],'(3)','LS','']).
%en:wrd([1,245,11,[0,0,0],' ','CD','']).
en:wrd([1,246,11,[0,0,0],'The','DT','']).
en:wrd([1,247,11,[0,0,0],'Minister','NNP','']).
en:wrd([1,248,11,[0,0,0],of,'IN','']).
en:wrd([1,249,11,[0,0,0],'Agriculture','NNP','']).
en:wrd([1,250,11,[0,0,0],',',',','']).
en:wrd([1,251,11,[0,0,0],'Forestry','NNP','']).
en:wrd([1,252,11,[0,0,0],and,'CC','']).
en:wrd([1,253,11,[0,0,0],'Fisheries','NNPS','']).
en:wrd([1,254,11,[0,0,0],shall,'MD','']).
en:wrd([1,255,11,[0,0,0],revise,'VB','']).
en:wrd([1,256,11,[0,0,0],the,'DT','']).
en:wrd([1,257,11,[0,0,0],basic,'JJ','']).
en:wrd([1,258,11,[0,0,0],policy,'NN','']).
en:wrd([1,259,11,[0,0,0],when,'WRB','']).
en:wrd([1,260,11,[0,0,0],necessary,'JJ','']).
en:wrd([1,261,11,[0,0,0],due,'JJ','']).
en:wrd([1,262,11,[0,0,0],to,'TO','']).
en:wrd([1,263,11,[0,0,0],changes,'NNS','']).
en:wrd([1,264,11,[0,0,0],in,'IN','']).
en:wrd([1,265,11,[0,0,0],the,'DT','']).
en:wrd([1,266,11,[0,0,0],'supply-and-demand','JJ','']).
en:wrd([1,267,11,[0,0,0],status,'NN','']).
en:wrd([1,268,11,[0,0,0],of,'IN','']).
en:wrd([1,269,11,[0,0,0],tuna,'NN','']).
en:wrd([1,270,11,[0,0,0],',',',','']).
en:wrd([1,271,11,[0,0,0],or,'CC','']).
en:wrd([1,272,11,[0,0,0],any,'DT','']).
en:wrd([1,273,11,[0,0,0],other,'JJ','']).
en:wrd([1,274,11,[0,0,0],circumstances,'NNS','']).
%en:wrd([1,275,11,[0,0,0],'.','.','']).

en_chunks(SentId, Chunks) :-
    findall([Content,FuncE],
        (
            en:wrd([_, _, SentId, _, Content, FuncE,_])
        ),
        Chunks).

en:cat(e1001, ['The','Minister','of','Agriculture',',','Forestry','and','Fisheries'], [np]).
en:cat(e1002, ['the','basic','policy'], [np]).
%en:cat(e1003, ['changes','in','the','supply-and-demand','status','of','tuna'], [np]).
en:cat(e1004, ['any','other','circumstances'], [np]).
en:cat(e2001, ['shall'], [fun(s, fun(s,np,b), b)]).
en:cat(e3001, ['revise'], [fun(fun(s,np,b), np, f)]).
en:cat(e4001, ['when','necessary'], [fun(s,s,f)]).
%en:cat(e4002, ['due','to'], [fun(s,s,f)]). %fun(np,np,f)]).
%en:cat(e4002, ['due','to'], [fun(np,np,f)]).
%en:cat(e5001, ['or'], [fun(fun(np,np,b), np, f)]).
% 1) or まわりの語彙をいったん無効化（この文のテストでは使わない）
%   % en:cat(e1003, [...], [np]).
%   % en:cat(e5001, ['or'], [fun(fun(np,np,b),np,f)]).
%   % en:cat(e1004, ['any','other','circumstances'], [np]).

% 2) まとめて副詞節として定義
en:cat(e4002,
  ['due','to','changes','in','the','supply-and-demand','status','of','tuna',',','or','any','other','circumstances'],
  [fun(s,s,f)]).

cat('DT',np).
cat('MD',fun(s, fun(s,np,b), b)).
cat('NNP',np).
cat('NN',np).
cat('NNS',np).
cat('NNPS',np).
%cat('WRB',np).
%cat('IN',np).
cat('TO',np).
cat('LS',np).
cat('CC',fun(fun(np,np,b), np, f)).
%cat('VB',np).
cat('JJ',np).
cat('CD',np).
cat(',',np).
cat('.',np).


combine(fun(X, Y, f), Y, X, 'Forward Application').
combine(Y, fun(X, Y, b), X, 'Backward Application').
combine(np, fun(s,np,f), s, '').
combine(s, fun(s,s,f), s, '').
combine(fun(s,s,f), s, s, '').
combine(fun(s,np,f), fun(s,s,f), fun(s,np,f), '').
combine(np, fun(fun(s,np,b),np,f), fun(s,np,b), '').
combine(fun(s,np,b), fun(s,np,b), fun(s,np,b), '').
combine(fun(s,np,b), fun(s,s,f), fun(s,np,b), '').
combine(s, fun(s,np,b), s, '').
combine(np, fun(fun(s,np,b),np,f), fun(s,np,b), '').
combine(fun(s,np,b), fun(s,np,b), fun(s,np,b), '').
combine(fun(s,np,b), fun(s,s,f), s, '').
combine(np, fun(s,s,f), np, '').
combine(fun(fun(s,np,b),np,f), fun(s,np,b), fun(s,np,b), '').
combine(np, s, s, '').
combine(np, np, np, '名詞句連接/弱い').
combine(s, s, s, '弱い結合').
combine(np, fun(s,np,b), s, '').
combine(fun(s,fun(s,np,b),b), fun(s,np,b), s, '').

%combine(fun(s,np,b), np, s, '').
%np x fun(s,np,b) --> s
%fun(s,np,b) x np --> s

myUnzip([],[]).
myUnzip([[H,_]|T],[H|T2]):- myUnzip(T,T2).

en_chunk_cat([], []).

en_chunk_cat(Chunk, [HF|TK]) :- 
  myUnzip(Chunk,OLS),
  append(LS,_,OLS),
  en:cat(ID,LS,[HF]),!,
  writeln([ID,LS,HF]),
  length(LS,LN),
  length(VR,LN),
  append(VR,T,Chunk),
  en_chunk_cat(T, TK). 

en_chunk_cat([[WD,TY]|T], [HF|TK]) :-
  cat(TY,HF),
  en_chunk_cat(T, TK). 

parse([C], C):- writeln([C,ok]).

parse(Cats, Result) :-
    reduce_leftmost(Cats, NewCats),
    length(NewCats,LN),
    format('~w, ~w ~n',[LN,NewCats]),
    parse(NewCats, Result).

reduce_leftmost([A,B|Rest], [C|Rest]) :-
    combine(A,B,C,NM),
    format("~w x ~w --> ~w     ~w~n", [A,B,C,NM]),
    !.

reduce_leftmost([X|Rest], [X|Rest2]) :-
    reduce_leftmost(Rest, Rest2).

en_ccg_11(Result) :-
    en_chunks(11, Chunks),
    writeln(Chunks),
    en_chunk_cat(Chunks, Cats),!,
    writeln(Cats),
    parse(Cats, Result).

