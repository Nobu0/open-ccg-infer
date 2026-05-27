%---------------------------------------
% メタ定義と関係情報をHTML表形式で出力する
% ファイル名: tool_mta_tbl.pl
% 入力データ:　prolog形式
% 出力データ:　HTML形式
% Date  :2017.2.18 by Nobuo Hamada
% MDate :2017.2.21 by Nobuo Hamada
%---------------------------------------
:- dynamic meta/3, mm/3, atr/3, vw/3. 
:- include('load_file.pl').
:- include('sub_htm_tbl.pl').

% 入力ファイルを読み込み関係データを取り出す  
main:-
  nb_setval(id,0),
  retractall(meta(_,_,_)),
  retractall(atr(_,_,_)),
  retractall(mm(_,_,_)),
  retractall(vw(_,_,_)),
  load_file('prolog/def_mta.pl'),
  write_file('prolog/mta_tbl.pl').

% 登録したデータから関係を取り出し、ファイルに結果を書き込む  
write_file(FL):-
  open(FL,write,Ot,[encoding(utf8)]),
  findall(LR,
     (mm(_,ML,MR),
      mm_fullname(ML,LL),
      mm_fullname(MR,RR),
      flatten([LL,RR],LR)),
  LS),
  %sort(LS,SO),
  nest_fill(5,LS,LS2),!,
  nest_rowspan(LS2,LH),!,
  %nest_rowspan2(LS3,LH),!,
  write_html(Ot,LH),
  close(Ot).

% メタ項目をエリアス名で置き換える 
mm_fullname(A,all):-
 var(A),!.
mm_fullname([],[]):-!.
mm_fullname(H,JN):-
  \+is_list(H),!,
  meta(_,H,JN).
mm_fullname([H,T],[HJ,Z]):-
  mm_fullname(H,HJ),!,
  mm_fullname(T,Z).
mm_fullname([H|T],[HJ|Z]):-
  mm_fullname(H,HJ),
  mm_fullname(T,Z).
  
:- main.

