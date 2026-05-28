%---------------------------------------
% メタ定義のエラー検査
% ファイル名: load_file.pl
% 入力データ:　prolog形式
% Date:2017.2.17 by Nobuo Hamada
%---------------------------------------

% ロードした関係にシーケンスIDを追加して登録する
% 重複チェックを行う
assert_id(TM):-  
  (call(TM)->
   format('worrning alredy exsist: ~p~n',[TM])
  ;get_id(ID),
   TM=..[_,ID|_],
   assert(TM)).

% ロードしたデータを登録する
% 重複チェックを行う
assert_cl(TM):-  
  (call(TM)->
   format('worrning alredy exsist: ~p~n',[TM])
  ;assert(TM)).

% 定義ファイルからデータを述語単位で読み込む  
load_file(FL):-
  open(FL,read,In,[encoding(utf8)]),
  repeat,
  (at_end_of_stream(In)->!
  ;read_clause(In,TM)->
   load_term(TM),
   fail
  ),
  close(In).

% メタ項目間は高次の関係にあるので、単体のメタ項目定義がされているか
% リストがネストしている部分を紐解いて１つに成ったら存在を確認する
chk_meta(A):- var(A),!.
chk_meta([]):-!.
chk_meta(H):-
  \+is_list(H),!,
  (meta(_,H,_)->!
  ;format('error not found: ~p~n',[H])).
chk_meta([H,T]):-
  chk_meta(H),!,
  chk_meta(T).
chk_meta([H|T]):-
  chk_meta(H),
  chk_meta(T).

chk_mmex(N,A,E):-
  (mm(_,A,_)->!
  ;mm(_,_,A)->!
  ;MA=..[mm,_|A],
   call(MA)->!
  ;format('warrning: ~d, ~p~n',[N,E])).

% メタ項目間で低次で対応付けがされているか検査  
chk_mm(mm(A,B)):-
  is_list(A),
  chk_mmex(1,A,mm(A,B)).
chk_mm(mm(A,B)):-
  is_list(B),
  chk_mmex(2,B,mm(A,B)).
chk_mm(mm(A,B)):-
  atom(A),
  var(B);atom(B).

  
% ロードしたデータがメタデータの中に定義されているか検査して、登録
load_term(meta(A,B)):-
  assert_id(meta(_,A,B)).
load_term(mm(A,B)):-
  chk_meta(A),
  chk_meta(B),
  chk_mm(mm(A,B)),!,
  assert_id(mm(_,A,B)).
load_term(atr(A,B)):-
  chk_meta(A),!,
  (meta(ID,A,_);mm(ID,A,_)),
  assert_cl(atr(ID,A,B)).
load_term(vw(A,B)):-
  chk_meta(A),
  chk_meta(B),!,
  (meta(ID,A,_);mm(ID,A,_)),
  assert_cl(vw(ID,A,B)).

% シーケンスIDを呼び出した時インクリメントし、取得  
get_id(ID):-
  nb_getval(id,I),
  ID is I+1,
  nb_setval(id,ID).

