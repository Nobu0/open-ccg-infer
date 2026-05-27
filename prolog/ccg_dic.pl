
ja:cat(j0001,['を超える'], [fun(fun(s, np, b), np, f)]).
ja:cat(j0002,['を超えない'], [fun(fun(s, np, b), np, f)]).
ja:cat(j0003,['を超えてはならない'], [fun(fun(s, np, b), np, f)]).
ja:cat(j0004,['を超えなければならない'], [fun(fun(s, np, b), np, f)]).
en:cat(j0001,['exceeding'], [fun(fun(s, np, b), np, f)]).
en:cat(j0002,['not', 'exceeding'], [fun(fun(s, np, b), np, f)]).
en:cat(j0003,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0004,[], [fun(fun(s, np, b), np, f)]).

ja:cat(j0005,['及び'], [fun(fun(np, np, b), np, f)]).
ja:cat(j0006,['かつ'], [fun(fun(np, np, b), np, f)]).
ja:cat(j0007,['若しくは'], [fun(fun(np, np, b), np, f)]).
ja:cat(j0008,['以上'], [fun(np, np, f)]).
ja:cat(j0009,['以下'], [fun(np, np, f)]).
ja:cat(j0010,['以内'], [fun(np, np, f)]).
ja:cat(j0011,['以外'], [fun(np, np, f)]).
ja:cat(j0012,['未満'], [fun(np, np, f)]).

en:cat(j0005,[or], [fun(fun(s, np, b), np, f)]).
en:cat(j0006,[and], [fun(fun(s, np, b), np, f)]).
en:cat(j0007,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0008,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0009,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0010,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0011,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0012,[], [fun(fun(s, np, b), np, f)]).

ja:cat(j0013,['しなければならない'], [fun(s, [fun(s,np,b), b)]).
ja:cat(j0014,['してはならない'], [fun(s, [fun(s,np,b), b)]).

en:cat(j0013,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0014,[], [fun(fun(s, np, b), np, f)]).

ja:cat(j0015,['することができる'], [fun(s, [fun(s,np,b), b)]).
ja:cat(j0016,['することができない'], [fun(s, [fun(s,np,b), b)]).
ja:cat(j0017,['することを妨げない'], [fun(s, [fun(s,np,b), b)]).
ja:cat(j0018,['することを要しない'], [fun(s, [fun(s,np,b), b)]).
ja:cat(j0019,['する必要がある'], [fun(s, [fun(s,np,b), b)]).
ja:cat(j0020,['するよう努めなければならない'], [fun(s, [fun(s,np,b), b)]).

en:cat(j0015,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0016,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0017,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0018,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0019,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0020,[], [fun(fun(s, np, b), np, f)]).

ja:cat(j0021,['に該当する'], [fun(np, np, f)]).
ja:cat(j0022,['当該'], [fun(np, np, f)]).
ja:cat(j0023,['に限り'], [fun(np, np, f)]).
ja:cat(j0024,['をいう'], [fun(np, np, b)]).
ja:cat(j0025,['とする'], [fun(np, np, b)]).

en:cat(j0021,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0022,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0023,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0024,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0025,[], [fun(fun(s, np, b), np, f)]).

% NP/NP 系
ja:cat(j0026,['から'], [fun(np,np,f)]).
ja:cat(j0027,['までの'], [fun(np,np,f)]).
ja:cat(j0028,['経過した'], [fun(np,np,f)]).
ja:cat(j0029,['超えない範囲内'], [fun(np,np,f)]).
ja:cat(j0030,['において'], [fun(np,np,f)]).
ja:cat(j0031,['もののほか'], [fun(np,np,f)]).
ja:cat(j0032,['による'], [fun(np,np,f)]).
ja:cat(j0033,['限り'], [fun(np,np,f)]).

en:cat(j0026,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0027,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0028,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0029,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0030,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0031,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0032,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0033,[], [fun(fun(s, np, b), np, f)]).


ja:cat(j0134,['を除くほか'], [fun(np,np,f)]).
ja:cat(j0135,['場合を除くほか'], [fun(np,np,f)]).

% j0134 = 例外
en:cat(j0134, ['except','as','otherwise','provided'], [fun(np,np,f)]).
en:cat(j0134, ['except','for'], [fun(np,np,f)]).
en:cat(j0134, ['other','than'], [fun(np,np,f)]).
% j0135 = 付加＋例外
en:cat(j0135, ['in','addition','to','the','cases'], [fun(np,np,f)]).
en:cat(j0135, ['except','when'], [fun(np,np,f)]).

% NP\NP 系（定義・規定）
ja:cat(j0034,['とあるのは'], [fun(np,np,b)]).
ja:cat(j0035,['ものとする'], [fun(np,np,b)]).
ja:cat(j0036,['意義は'], [fun(np,np,b)]).
ja:cat(j0037,['ところによる'], [fun(np,np,b)]).
ja:cat(j0038,['という'], [fun(np,np,b)]).

en:cat(j0034,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0035,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0036,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0037,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0038,[], [fun(fun(s, np, b), np, f)]).

% --- NP/NP 系 ---
ja:cat(j0039,['から施行する'], [fun(np,np,f)]).
ja:cat(j0040,['目的とする'], [fun(np,np,f)]).
ja:cat(j0041,['のため'], [fun(np,np,f)]).
ja:cat(j0042,['規定により'], [fun(np,np,f)]).
ja:cat(j0043,['するほか'], [fun(np,np,f)]).
ja:cat(j0044,['限りでない'], [fun(np,np,f)]).
ja:cat(j0045,['遅滞なく'], [fun(np,np,f)]).

en:cat(j0039,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0040,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0041,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0042,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0043,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0044,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0045,[], [fun(fun(s, np, b), np, f)]).

% --- NP\NP 系（後ろ向き） ---
ja:cat(j0046,['効力を失う'], [fun(np,np,b)]).
ja:cat(j0047,['定めるものとする'], [fun(np,np,b)]).
ja:cat(j0048,['規定する'], [fun(np,np,b)]).
ja:cat(j0049,['規定する場合において'], [fun(np,np,b)]).
ja:cat(j0050,['したときは'], [fun(np,np,b)]).

en:cat(j0046,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0047,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0048,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0049,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0050,[], [fun(fun(s, np, b), np, f)]).

% --- 文レベルの例外規定 ---
ja:cat(j0051,['ただし'], [fun(s, [fun(s,np,b),b)]).

en:cat(j0051,[';', provided, however, that], [fun(fun(s, np, b), np, f)]).

ja:cat(j0052,['、'], [fun(fun(np,np,b),np,f)]).
ja:cat(j0053,['等'], [fun(fun(np,np,b),np,f)]).
ja:cat(j0054,['又'], [fun(fun(np,np,b),np,f)]).
ja:cat(j0055,['又は'], [fun(fun(np,np,b),np,f)]).
ja:cat(j0056,['並びに'], [fun(fun(np,np,b),np,f)]).

en:cat(j0052,[','], [fun(fun(s, np, b), np, f)]).
en:cat(j0053,[',', 'etc.'], [fun(fun(s, np, b), np, f)]).
en:cat(j0054,[or], [fun(fun(s, np, b), np, f)]).
en:cat(j0055,[or], [fun(fun(s, np, b), np, f)]).
en:cat(j0056,[and], [fun(fun(s, np, b), np, f)]).

ja:cat(j0057,['当分の間'], [fun(np,np,f)]).
ja:cat(j0058,['なおその効力を有する'], [fun(np,np,f)]).
ja:cat(j0059,['みだりに'], [fun(np,np,f)]).

en:cat(j0057,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0058,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0059,[], [fun(fun(s, np, b), np, f)]).

ja:cat(j0060,['同様とする'], [fun(np,np,b)]).
ja:cat(j0061,['とする'], [fun(np,np,b)]).   % 既存
ja:cat(j0062,['みなす'], [fun(np,np,b)]).

en:cat(j0060,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0061,[], [fun(fun(s, np, b), np, f)]).
en:cat(j0062,[], [fun(fun(s, np, b), np, f)]).

ja:cat(j1001,['において準用する',_,'の規定'], [fun(np,np,f)]).
ja:cat(j1002,['については、',_,'の例による'], [fun(np,np,f)]).
ja:cat(j1003,['の規定は、',_,'について準用する'], [fun(np,np,f)]).

en:cat(j1001,[], [fun(fun(s, np, b), np, f)]).
en:cat(j1002,[], [fun(fun(s, np, b), np, f)]).
en:cat(j1003,[], [fun(fun(s, np, b), np, f)]).

ja:cat(j1004,['において準用する',_,'の規定'], [fun(np,np,f)]).
ja:cat(j1005,['については、',_,'の例による'], [fun(np,np,f)]).
ja:cat(j1006,['の規定は、',_,'について準用する'], [fun(np,np,f)]).
ja:cat(j1007,['の規定に違反して',_,'した者'], [fun(np,np,f)]).
ja:cat(j1008,['の日の',_,'日前までに'], [fun(np,np,f)]).
ja:cat(j1009,['は、',_,'と解釈してはならない'], [fun(np,np,f)]).

en:cat(j1004,[], [fun(fun(s, np, b), np, f)]).
en:cat(j1005,[], [fun(fun(s, np, b), np, f)]).
en:cat(j1006,[], [fun(fun(s, np, b), np, f)]).
en:cat(j1007,[], [fun(fun(s, np, b), np, f)]).
en:cat(j1008,[], [fun(fun(s, np, b), np, f)]).
en:cat(j1009,[], [fun(fun(s, np, b), np, f)]).

ja:cat(j1010,['なおその効力を有する'],[fun()]).
ja:cat(j1011,['並びに'],[fun()]).
ja:cat(j1012,['において準用する',_,'の規定'],[fun()]).
ja:cat(j1013,['において準用する場合を含む'],[fun()]).
ja:cat(j1014,['に掲げる事項'],[fun()]).
ja:cat(j1015,['に掲げるもののほか'],[fun()]).
ja:cat(j1016,['に係る'],[fun()]).
ja:cat(j1017,['に限る'],[fun()]).
ja:cat(j1018,['に代わる'],[fun()]).
ja:cat(j1019,['に関連する事項'],[fun()]).
ja:cat(j1020,['に定めるところにより'],[fun()]).
ja:cat(j1021,['に従わないで'],[fun()]).
ja:cat(j1022,['に準ずる'],[fun()]).
ja:cat(j1023,['に処する'],[fun()]).
ja:cat(j1024,['については、',_,'の例による'],[fun()]).
ja:cat(j1025,['については、なお従前の例による'],[fun()]).
ja:cat(j1026,['に照らし'],[fun()]).
ja:cat(j1027,['に満たない'],[fun()]).
ja:cat(j1028,['に基づく'],[fun()]).
ja:cat(j1029,['のいずれかに該当する'],[fun()]).
ja:cat(j1030,['の規定に違反して',_,'した者'],[fun()]).
ja:cat(j1031,['の規定にかかわらず'],[fun()]).
ja:cat(j1032,['の規定により'],[fun()]).
ja:cat(j1033,['の規定は、',_,'について準用する'],[fun()]).
ja:cat(j1034,['の規定は、',_,'についても適用する'],[fun()]).
ja:cat(j1035,['の日の',_,'日前までに'],[fun()]).
ja:cat(j1036,['の日の翌日から起算して'],[fun()]).
ja:cat(j1037,['は、',_,'と解釈してはならない'],[fun()]).
ja:cat(j1038,['は、',_,'と認めるときは'],[fun()]).
ja:cat(j1039,['は、他の法律に特別の定めのある場合を除くほか、この法律の定めるところによる'],[fun()]).
ja:cat(j1040,['不服を申し立てることができない'],[fun()]).
ja:cat(j1041,['別段の定めがある場合を除き'],[fun()]).
ja:cat(j1042,['別に法律で定める日'],[fun()]).

en:cat(j1010,[], [fun(fun(s, np, b), np, f)]).
en:cat(j1011,[], [fun(fun(s, np, b), np, f)]).
en:cat(j1012,[], [fun(fun(s, np, b), np, f)]).
en:cat(j1013,[], [fun(fun(s, np, b), np, f)]).
en:cat(j1014,[], [fun(fun(s, np, b), np, f)]).
en:cat(j1015,[], [fun(fun(s, np, b), np, f)]).
en:cat(j1016,[], [fun(fun(s, np, b), np, f)]).
en:cat(j1017,[], [fun(fun(s, np, b), np, f)]).
en:cat(j1018,[], [fun(fun(s, np, b), np, f)]).
en:cat(j1019,[], [fun(fun(s, np, b), np, f)]).
en:cat(j1020,[], [fun(fun(s, np, b), np, f)]).
en:cat(j1021,[], [fun(fun(s, np, b), np, f)]).
en:cat(j1022,[], [fun(fun(s, np, b), np, f)]).
en:cat(j1023,[], [fun(fun(s, np, b), np, f)]).
en:cat(j1024,[], [fun(fun(s, np, b), np, f)]).
en:cat(j1025,[], [fun(fun(s, np, b), np, f)]).
en:cat(j1026,[], [fun(fun(s, np, b), np, f)]).
en:cat(j1027,[], [fun(fun(s, np, b), np, f)]).
en:cat(j1028,[], [fun(fun(s, np, b), np, f)]).
en:cat(j1029,[], [fun(fun(s, np, b), np, f)]).
en:cat(j1030,[], [fun(fun(s, np, b), np, f)]).
en:cat(j1031,[], [fun(fun(s, np, b), np, f)]).
en:cat(j1032,[], [fun(fun(s, np, b), np, f)]).
en:cat(j1033,[], [fun(fun(s, np, b), np, f)]).
en:cat(j1034,[], [fun(fun(s, np, b), np, f)]).
en:cat(j1035,[], [fun(fun(s, np, b), np, f)]).
en:cat(j1036,[], [fun(fun(s, np, b), np, f)]).
en:cat(j1037,[], [fun(fun(s, np, b), np, f)]).
en:cat(j1038,[], [fun(fun(s, np, b), np, f)]).
en:cat(j1039,[], [fun(fun(s, np, b), np, f)]).
en:cat(j1040,[], [fun(fun(s, np, b), np, f)]).
