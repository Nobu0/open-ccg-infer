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


morph([1,249,11,[0,0,0],'３',cd,'名詞,数']).
morph([1,250,11,[0,0,0],'　',sp,'記号,空白']).
morph([1,251,11,[0,0,0],農林,nn,'名詞,一般']).
morph([1,252,11,[0,0,0],水産,nn,'名詞,一般']).
morph([1,253,11,[0,0,0],大臣,nn,'名詞,一般']).
morph([1,254,11,[0,0,0],は,係,'助詞,係助詞']).
morph([1,255,11,[0,0,0],'、',',','記号,読点']).
morph([1,256,11,[0,0,0],まぐろ,nn,'名詞,一般']).
morph([1,257,11,[0,0,0],資源,nn,'名詞,一般']).
morph([1,258,11,[0,0,0],の,の,'助詞,連体化']).
morph([1,259,11,[0,0,0],動向,nn,'名詞,一般']).
morph([1,260,11,[0,0,0],'、',',','記号,読点']).
morph([1,261,11,[0,0,0],まぐろ,nn,'名詞,一般']).
morph([1,262,11,[0,0,0],の,の,'助詞,連体化']).
morph([1,263,11,[0,0,0],需給,nn,'名詞,一般']).
morph([1,264,11,[0,0,0],事情,nn,'名詞,一般']).
morph([1,265,11,[0,0,0],その他,nnd,'名詞,代名詞']).
morph([1,266,11,[0,0,0],の,の,'助詞,連体化']).
morph([1,267,11,[0,0,0],事情,nn,'名詞,一般']).
morph([1,268,11,[0,0,0],の,の,'助詞,連体化']).
morph([1,269,11,[0,0,0],変動,nns,'名詞,サ変接続']).
morph([1,270,11,[0,0,0],により,格,'助詞,格助詞']).
morph([1,271,11,[0,0,0],必要,nnjv,'名詞,形容動詞語幹']).
morph([1,272,11,[0,0,0],が,格,'助詞,格助詞']).
morph([1,273,11,[0,0,0],ある,vb,'動詞,自立']).
morph([1,274,11,[0,0,0],とき,nnh,'名詞,非自立']).
morph([1,275,11,[0,0,0],は,係,'助詞,係助詞']).
morph([1,276,11,[0,0,0],'、',',','記号,読点']).
morph([1,277,11,[0,0,0],基本,nn,'名詞,一般']).
morph([1,278,11,[0,0,0],方針,nn,'名詞,一般']).
morph([1,279,11,[0,0,0],を,格,'助詞,格助詞']).
morph([1,280,11,[0,0,0],変更,nns,'名詞,サ変接続']).
morph([1,281,11,[0,0,0],する,vb,'動詞,自立']).
morph([1,282,11,[0,0,0],もの,nnh,'名詞,非自立']).
morph([1,283,11,[0,0,0],と,格,'助詞,格助詞']).
morph([1,284,11,[0,0,0],する,vb,'動詞,自立']).
morph([1,285,11,[0,0,0],'。','.','記号,句点']).

/*

jp_chunks(SentId, Chunks) :-
    findall(JChunk, jewd(SentId, JChunk, _, _, _), Chunks).

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
jp_chunk_cat([、], fun(s,s,f)).
*/
%jp_chunks(11, Chunks),
%maplist(jp_chunk_cat, Chunks, Cats),
%parse(Cats, S).

% ---- 前向き適用: (X/Y) Y => X ----
combine(fun(X, Y, f), Y, X).

% ---- 後ろ向き適用: Y (X\Y) => X ----
combine(Y, fun(X, Y, b), X).

% parse(+Cats, -ResultCat)
% Cats: [Cat1, Cat2, ...]

parse([C], C).  % 1 つだけならそれが結果

parse(Cats, Result) :-
    % 隣り合う 2 つを選んで combine
    append(Left, [A,B|Right], Cats),
    combine(A, B, C),
    %writeln([A,B,'->',C]),
    append(Left, [C|Right], NewCats),
    length(NewCats,LN),
    %format('~w, ',[LN]),
    parse(NewCats, Result).


jp_chunks(SentId, Chunks) :-
    findall(Chunk,
        (
            jewd(SentId, Content, FuncJ, _FuncE, _Eng),
            append(Content, FuncJ, Chunk)
        ),
        Chunks).

% --- 名詞句 ---
jp_chunk_cat(Chunk, np) :-
    Chunk = [W|_],
    ja:wrd([_,_,_,_,W,_,Pos]),
    sub_atom(Pos, 0, _, _, '名詞').

% --- 助詞を含む複合チャンク ---
jp_chunk_cat(Chunk, fun(s,np,f)) :- member(は, Chunk).
jp_chunk_cat(Chunk, fun(fun(s,np,b), np, f)) :- member(を, Chunk).
jp_chunk_cat(Chunk, fun(fun(s,np,b), np, f)) :- member(が, Chunk).
jp_chunk_cat(Chunk, fun(fun(s,np,b), np, f)) :- member(により, Chunk).

% --- 動詞を含むチャンク ---
jp_chunk_cat(Chunk, fun(s,np,b)) :- member(ある, Chunk).
jp_chunk_cat(Chunk, fun(s,np,b)) :- member(する, Chunk).

% --- 記号 ---
jp_chunk_cat(Chunk, fun(s,s,f)) :- member('、', Chunk).
jp_chunk_cat(Chunk, fun(s,s,f)) :- member('。', Chunk).
jp_chunk_cat(['３','　'], fun(s,s,f)).

jp_ccg(SentId, Result) :-
    jp_chunks(SentId, Chunks),
    maplist(jp_chunk_cat, Chunks, Cats),
    writeln(Cats),
    parse(Cats, Result).

:- jp_ccg(11, S), writeln(S).



/*


sent_jp(11, Tokens) :-
    findall(JChunk,
            jewd(11, JChunk, _JFunc, _EFunc, _EChunk),
            Chunks),
    append(Chunks, Tokens).

?- sent_jp(11, Toks), writeln(Toks).
% ---- カテゴリ表現 ----
% 原始カテゴリ
cat(s).
cat(np).
cat(n).

% 句カテゴリ：X/Y や X\Y を fun(X, Y, Dir) で表現
% Dir は f(前向き) / b(後ろ向き)
cat(fun(X,Y,_)) :- cat(X), cat(Y).

% "The Minister revised the basic policy."
% みたいな超単純化例

lex(the, fun(np, n, f)).
lex(minister, n).
lex(revised, fun(fun(s, np, b), np, f)).  % ((S\NP)/NP)
lex(basic, fun(n, n, f)).
lex(policy, n).

sentence([the, minister, revised, the, basic, policy]).

sentence_cat(Sent, Cat) :-
    maplist(lex, Sent, Cats),
    writeln(Cats),
    parse(Cats, Cat).

?- sentence(S), sentence_cat(S, Cat), writeln(Cat).
%S = [the, minister, revised, the, basic, policy],
%Cat = s.
*/