%---------------------------------------
% メタ定義と関係情報をHTML表形式で出力する
% ファイル名: sub_htm_tbl.pl
% 入力データ:　prolog形式
% 出力データ:　HTML形式
% Date  :2017.2.18 by Nobuo Hamada
% MDate :2017.2.20 by Nobuo Hamada
%---------------------------------------

% HTML形式で出力  
write_html(Ot,LS):-  
  html_tag(['table',' class="tbl2"'],HA),
  format(Ot,'~w~n',[HA]),
  maplist(html_tr,LS,LH),
  maplist(format(Ot,'~w~n'),LH),
  html_tag(['/table'],TA),
  format(Ot,'~w~n',[TA]).

% TR部分の生成  
html_tr(S,D):-
  %writeln(S),
  (S=1:S2->html_td(S2,D1)
  ;html_td(S,D1)),
  html_tag2([tr],D1,D).

% TDとROWSPANを生成  
html_td_span(N,H,TAG):-
  html_tag2([td,' rowspan=',N],H,TAG).

% TDを生成
html_td([],[]):-!.
html_td(_:[],[]):-!.
html_td(N:[H|T],[HTM|X]):-
  dif(H,' '),
  html_td_span(N,H,HTM),
  html_td(N:T,X).
html_td(_:[H|T],[HTM|X]):-
  html_tag2(td,H,HTM),
  html_td(T,X).
html_td([H|T],[HTM|X]):-
  html_tag2(td,H,HTM),
  html_td(T,X).

% タグを生成する  
html_tag(TG,AT):-
  append([['<'],TG,['>']],LS), 
  atomic_list_concat(LS,AT).

%　タグで囲む  
html_tag2([TG|Z],A,FM):- 
  html_tag([TG|Z],HD), 
  html_tag(['/',TG],TL),
  flatten([HD,A,TL],FL),  
  atomic_list_concat(FL,FM).
html_tag2(TG,A,FM):- 
  html_tag([TG],HD), 
  html_tag(['/',TG],TL), 
  atomic_list_concat([HD,A,TL],FM).

% 後ろに空白で固定長になるまで埋める  
set_fill(M,S,D):-
  length(S,L),
  LN is M-L,
  LN>=0,
  sub_atom('     ',0,LN,_,SP),
  atom_chars(SP,LSP),
  append(S,LSP,D).
set_fill(_,S,S).
  
% 行方向に同じメタ項目が存在している数情報を追加（デフォルトは１）  
nest_fill(_,[],[]).
nest_fill(M,[H|T],[HP|X]):-
  set_fill(M,H,HP),
  nest_fill(M,T,X).

% 後ろの空白を削除する
trim([],[]).
trim([' '|T],X):- trim(T,X).
trim([H|T],[H|X]):- trim(T,X).

% ROWSPANを求める  
nest_rowspan([],[]).
nest_rowspan([H|T],[R:H|X]):-
  trim(H,HP),
  get_rowspan(R,HP,T,TN),
  nest_rowspan(TN,X).

% 下方向へ検索し数を求め,セルを削除する  
get_rowspan(I,K,[H|T],[REM|X]):-
  append(K,REM,H),
  get_rowspan(I2,K,T,X),
  I is I2+1.
get_rowspan(1,_,X,X).