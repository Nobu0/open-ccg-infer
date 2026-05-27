jewd(11,['３','　'],[],            [],['(3)',' ']).
jewd(11,[農林,水産,大臣],[は,、],  ['The'],['Minister',of,'Agriculture',',','Forestry',and,'Fisheries']).
jewd(11,[まぐろ],[資源,の,動向,、,まぐろ,の],[status,of],[tuna]).
jewd(11,[需給],[],                 [in,the],['supply-and-demand']).
jewd(11,[事情],[],                 [],[circumstances]).
jewd(11,[その他],[の,事情,の],     [',',or,any],[other]).
jewd(11,[変動],[],                 [],[changes]).
jewd(11,[により],[],               [],[due,to]).
jewd(11,[必要],[が,ある],          [],[necessary]).
jewd(11,[とき],[は,、],            [],[when]).
jewd(11,[基本,方針],[を],          [the],[basic,policy]).
jewd(11,[変更],[する],             [],[revise]).
jewd(11,[もの,と,する],[],         [],[shall]).
jewd(11,[。],[],                   [],['.']).

ja:wrd([1,249,11,[0,0,0],'３',cd,'名詞,数']).
ja:wrd([1,250,11,[0,0,0],'　',sp,'記号,空白']).
ja:wrd([1,251,11,[0,0,0],農林,nn,'名詞,一般']).
ja:wrd([1,252,11,[0,0,0],水産,nn,'名詞,一般']).
ja:wrd([1,253,11,[0,0,0],大臣,nn,'名詞,一般']).
ja:wrd([1,254,11,[0,0,0],は,係,'助詞,係助詞']).
ja:wrd([1,255,11,[0,0,0],'、',',','記号,読点']).
ja:wrd([1,256,11,[0,0,0],まぐろ,nn,'名詞,一般']).
ja:wrd([1,257,11,[0,0,0],資源,nn,'名詞,一般']).
ja:wrd([1,258,11,[0,0,0],の,の,'助詞,連体化']).
ja:wrd([1,259,11,[0,0,0],動向,nn,'名詞,一般']).
ja:wrd([1,260,11,[0,0,0],'、',',','記号,読点']).
ja:wrd([1,261,11,[0,0,0],まぐろ,nn,'名詞,一般']).
ja:wrd([1,262,11,[0,0,0],の,の,'助詞,連体化']).
ja:wrd([1,263,11,[0,0,0],需給,nn,'名詞,一般']).
ja:wrd([1,264,11,[0,0,0],事情,nn,'名詞,一般']).
ja:wrd([1,265,11,[0,0,0],その他,nnd,'名詞,代名詞']).
ja:wrd([1,266,11,[0,0,0],の,の,'助詞,連体化']).
ja:wrd([1,267,11,[0,0,0],事情,nn,'名詞,一般']).
ja:wrd([1,268,11,[0,0,0],の,の,'助詞,連体化']).
ja:wrd([1,269,11,[0,0,0],変動,nns,'名詞,サ変接続']).
ja:wrd([1,270,11,[0,0,0],により,格,'助詞,格助詞']).
ja:wrd([1,271,11,[0,0,0],必要,nnjv,'名詞,形容動詞語幹']).
ja:wrd([1,272,11,[0,0,0],が,格,'助詞,格助詞']).
ja:wrd([1,273,11,[0,0,0],ある,vb,'動詞,自立']).
ja:wrd([1,274,11,[0,0,0],とき,nnh,'名詞,非自立']).
ja:wrd([1,275,11,[0,0,0],は,係,'助詞,係助詞']).
ja:wrd([1,276,11,[0,0,0],'、',',','記号,読点']).
ja:wrd([1,277,11,[0,0,0],基本,nn,'名詞,一般']).
ja:wrd([1,278,11,[0,0,0],方針,nn,'名詞,一般']).
ja:wrd([1,279,11,[0,0,0],を,格,'助詞,格助詞']).
ja:wrd([1,280,11,[0,0,0],変更,nns,'名詞,サ変接続']).
ja:wrd([1,281,11,[0,0,0],する,vb,'動詞,自立']).
ja:wrd([1,282,11,[0,0,0],もの,nnh,'名詞,非自立']).
ja:wrd([1,283,11,[0,0,0],と,格,'助詞,格助詞']).
ja:wrd([1,284,11,[0,0,0],する,vb,'動詞,自立']).
ja:wrd([1,285,11,[0,0,0],'。','.','記号,句点']).
ja:wrd([1,263,11,[0,0,0],像,nn,'名詞,一般']).
ja:wrd([1,263,11,[0,0,0],鼻,nn,'名詞,一般']).
ja:wrd([1,263,11,[0,0,0],長い,jj,'形容詞/述語']).

chunks_1([
 [像], [が], [鼻], [が], [長い]
% [像], [は], [鼻], [が], [長い]
 ]).


chunks_11([['３','　'],
 [農林,水産,大臣], [は], ['、'],
 [まぐろ,資源,の,動向],
 ['、'],
 [まぐろ,の],
 [需給],
 [事情],
 [その他,の,事情,の],
 [変動],
 [により],
 [必要,が,ある],
 [とき], [は], ['、'],
 [基本,方針], [を],
 [変更,する],
 [もの,と,する],
 ['。']]).



jp_chunks(SentId, Chunks) :-
    findall(Chunk,
        (
            jewd(SentId, Content, FuncJ, _FuncE, _Eng),
            append(Content, FuncJ, Chunk)
        ),
        Chunks).
/*
jp_chunk_cat(['３','　'], fun(s,s,f)).
jp_chunk_cat([農林,水産,大臣], np).
jp_chunk_cat([まぐろ], np).
jp_chunk_cat([需給], np).
jp_chunk_cat([事情], np).
jp_chunk_cat([その他], np).
jp_chunk_cat([変動], np).
jp_chunk_cat([により], fun(fun(s,np,b), np, f)).
jp_chunk_cat([必要], fun(s,np,b)).
jp_chunk_cat([とき], np).
jp_chunk_cat([基本,方針], np).
jp_chunk_cat([変更], fun(fun(s,np,b), np, f)).
jp_chunk_cat([もの,と,する], fun(s,np,b)).
jp_chunk_cat(['。'], fun(s,s,f)).

jp_chunk_cat([は], fun(s,np,f)).
jp_chunk_cat([を], fun(fun(s,np,b), np, f)).
jp_chunk_cat([が], fun(fun(s,np,b), np, f)).
jp_chunk_cat(['、'], fun(s,s,f)).

*/



% --- 助詞を含む複合チャンク ---
jp_chunk_cat(Chunk, fun(s,np,b)) :- member(長い, Chunk).
jp_chunk_cat(Chunk, fun(s,np,f)) :- member(は, Chunk).
jp_chunk_cat(Chunk, fun(fun(s,np,b), np, f)) :- member('を', Chunk).
jp_chunk_cat(Chunk, fun(fun(s,np,b), np, f)) :- member(により, Chunk).
jp_chunk_cat(Chunk, KX) :-
  member(が, Chunk),
  (KX=fun(s, np, b)
  ;KX=fun(np,np,f)).

% --- 動詞を含むチャンク ---
jp_chunk_cat(Chunk, fun(s,np,b)) :- member(ある, Chunk).
% 「ものとする」は VP（S\NP）
jp_chunk_cat(Chunk, fun(s,np,b)) :-
    member(もの, Chunk),
    member(する, Chunk).

% 「変更する」など通常の動詞句も VP
jp_chunk_cat(Chunk, fun(s,np,b)) :-
    member(する, Chunk).

%jp_chunk_cat(Chunk, fun(s,np,b)) :- member(する, Chunk).

% --- 記号 ---
%jp_chunk_cat(Chunk, fun(s,s,f)) :- member('、', Chunk).
jp_chunk_cat(Chunk, fun(s,s,f)) :- member('。', Chunk).
jp_chunk_cat(Chunk, np) :- get_wrdpo(Chunk,cd).
jp_chunk_cat(['、'], fun(s,s,f)).
jp_chunk_cat(['。'], fun(s,s,f)).

jp_chunk_cat(Chunk, np) :-
   member(W,Chunk), 
   get_wrdpo([W],PO),
   member(PO,[nn,nnjv,nnh,nnd,nns,'の','、']).

get_wrdpo([W|_],PO):-
  %writeln(W), 
  ja:wrd([_,_,_,_,W,PO|_]).
get_wrdpo(_,np).

cat(s).
cat(np).
cat(n).

% 句カテゴリ：X/Y や X\Y を fun(X, Y, Dir) で表現
% Dir は f(前向き) / b(後ろ向き)
cat(fun(X,Y,_)) :- cat(X), cat(Y).

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


% parse(+Cats, -ResultCat)
% Cats: [Cat1, Cat2, ...]

parse([C], C):- writeln([C,ok]).

parse(Cats, Result) :-
    reduce_leftmost(Cats, NewCats),
    length(NewCats,LN),
    %format('~w, ~w ~n',[LN,NewCats]),
    parse(NewCats, Result).

reduce_leftmost([A,B|Rest], [C|Rest]) :-
    combine(A,B,C,NM),
    %format("~w x ~w --> ~w     ~w~n", [A,B,C,NM]).
    !.

reduce_leftmost([X|Rest], [X|Rest2]) :-
    reduce_leftmost(Rest, Rest2).

jp_ccg_11(Result) :-
    chunks_11(Chunks),
    writeln(Chunks),
    maplist(jp_chunk_cat, Chunks, Cats),!,
    writeln(Cats),
    parse(Cats, Result).

jp_ccg_1(Result) :-
    chunks_1(Chunks),
    writeln(Chunks),
    maplist(jp_chunk_cat, Chunks, Cats),
    format("-- Cat:~w -----~n",[Cats]),
    parse(Cats, Result),false;true.
