
ja:cat(j0001,['を超える'], ['(S\NP)/NP']).
ja:cat(j0002,['を超えない'], ['(S\NP)/NP']).
ja:cat(j0003,['を超えてはならない'], ['(S\NP)/NP']).
ja:cat(j0004,['を超えなければならない'], ['(S\NP)/NP']).
en:cat(j0001,['exceeding'], ['(S\NP)/NP']).
en:cat(j0002,['not', 'exceeding'], ['(S\NP)/NP']).
en:cat(j0003,[], ['(S\NP)/NP']).
en:cat(j0004,[], ['(S\NP)/NP']).

ja:cat(j0005,['及び'], ['(NP\NP)/NP']).
ja:cat(j0006,['かつ'], ['(NP\NP)/NP']).
ja:cat(j0007,['若しくは'], ['(NP\NP)/NP']).
ja:cat(j0008,['以上'], ['NP/NP']).
ja:cat(j0009,['以下'], ['NP/NP']).
ja:cat(j0010,['以内'], ['NP/NP']).
ja:cat(j0011,['以外'], ['NP/NP']).
ja:cat(j0012,['未満'], ['NP/NP']).

en:cat(j0005,[or], ['(S\NP)/NP']).
en:cat(j0006,[and], ['(S\NP)/NP']).
en:cat(j0007,[], ['(S\NP)/NP']).
en:cat(j0008,[], ['(S\NP)/NP']).
en:cat(j0009,[], ['(S\NP)/NP']).
en:cat(j0010,[], ['(S\NP)/NP']).
en:cat(j0011,[], ['(S\NP)/NP']).
en:cat(j0012,[], ['(S\NP)/NP']).

ja:cat(j0013,['なければならない'], ['S\(S\NP)'],['助動', '接', 'vbo', '助動']).
ja:cat(j0014,['てはならない'], ['S\(S\NP)'],['接', '係', 'vbo', '助動']).

en:cat(j0013,[], ['(S\NP)/NP']).
en:cat(j0014,[], ['(S\NP)/NP']).

ja:cat(j0015,['することができる'], ['S\(S\NP)']).
ja:cat(j0016,['することができない'], ['S\(S\NP)']).
ja:cat(j0017,['することを妨げない'], ['S\(S\NP)']).
ja:cat(j0018,['することを要しない'], ['S\(S\NP)']).
ja:cat(j0019,['する必要がある'], ['S\(S\NP)']).
ja:cat(j0020,['するよう努めなければならない'], ['S\(S\NP)']).

en:cat(j0015,[], ['(S\NP)/NP']).


,[], ['(S\NP)/NP']).
,[], ['(S\NP)/NP']).
en:cat(j0020,[], ['(S\NP)/NP']).

ja:cat(j0021,['に該当する'], ['NP/NP']).
ja:cat(j0022,['当該'], ['NP/NP']).
ja:cat(j0023,['に限り'], ['NP/NP']).
ja:cat(j0024,['をいう'], [fun(np, np, b)]).
ja:cat(j0025,['とする'], [fun(np, np, b)]).

en:cat(j0021,[], ['(S\NP)/NP']).
en:cat(j0022,[], ['(S\NP)/NP']).
en:cat(j0023,[], ['(S\NP)/NP']).
en:cat(j0024,[], ['(S\NP)/NP']).
en:cat(j0025,[], ['(S\NP)/NP']).

% NP/NP 系
ja:cat(j0026,['から'], ['NP/NP']).
ja:cat(j0027,['までの'], ['NP/NP']).
ja:cat(j0028,['経過した'], ['NP/NP']).
ja:cat(j0029,['超えない範囲内'], ['NP/NP']).
ja:cat(j0030,['において'], ['NP/NP']).
ja:cat(j0031,['もののほか'], ['NP/NP']).
ja:cat(j0032,['による'], ['NP/NP']).
ja:cat(j0033,['限り'], ['NP/NP']).

en:cat(j0026,[], ['(S\NP)/NP']).
en:cat(j0027,[], ['(S\NP)/NP']).
en:cat(j0028,[], ['(S\NP)/NP']).
en:cat(j0029,[], ['(S\NP)/NP']).
en:cat(j0030,[], ['(S\NP)/NP']).
en:cat(j0031,[], ['(S\NP)/NP']).
en:cat(j0032,[], ['(S\NP)/NP']).
en:cat(j0033,[], ['(S\NP)/NP']).


ja:cat(j0134,['を除くほか'], ['NP/NP']).
ja:cat(j0135,['場合を除くほか'], ['NP/NP']).

% j0134 = 例外
en:cat(j0134, ['except','as','otherwise','provided'], ['NP/NP']).
en:cat(j0134, ['except','for'], ['NP/NP']).
en:cat(j0134, ['other','than'], ['NP/NP']).
% j0135 = 付加＋例外
en:cat(j0135, ['in','addition','to','the','cases'], ['NP/NP']).
en:cat(j0135, ['except','when'], ['NP/NP']).

% NP\NP 系（定義・規定）
ja:cat(j0034,['とあるのは'], ['NP\NP']).
ja:cat(j0035,['ものとする'], ['NP\NP']).
ja:cat(j0036,['意義は'], ['NP\NP']).
ja:cat(j0037,['ところによる'], ['NP\NP']).
ja:cat(j0038,['という'], ['NP\NP']).

en:cat(j0034,[], ['(S\NP)/NP']).
en:cat(j0035,[], ['(S\NP)/NP']).
en:cat(j0036,[], ['(S\NP)/NP']).
en:cat(j0037,[], ['(S\NP)/NP']).
en:cat(j0038,[], ['(S\NP)/NP']).

% --- NP/NP 系 ---
ja:cat(j0039,['から施行する'], ['NP/NP']).
ja:cat(j0040,['目的とする'], ['NP/NP']).
ja:cat(j0041,['のため'], ['NP/NP']).
ja:cat(j0042,['規定により'], ['NP/NP']).
ja:cat(j0043,['するほか'], ['NP/NP']).
ja:cat(j0044,['限りでない'], ['NP/NP']).
ja:cat(j0045,['遅滞なく'], ['NP/NP']).

en:cat(j0039,[], ['(S\NP)/NP']).
en:cat(j0040,[], ['(S\NP)/NP']).
en:cat(j0041,[], ['(S\NP)/NP']).
en:cat(j0042,[], ['(S\NP)/NP']).
en:cat(j0043,[], ['(S\NP)/NP']).
en:cat(j0044,[], ['(S\NP)/NP']).
en:cat(j0045,[], ['(S\NP)/NP']).

% --- NP\NP 系（後ろ向き） ---
ja:cat(j0046,['効力を失う'], ['NP\NP']).
ja:cat(j0047,['定めるものとする'], ['NP\NP']).
ja:cat(j0048,['規定する'], ['NP\NP']).
ja:cat(j0049,['規定する場合において'], ['NP\NP']).
ja:cat(j0050,['したときは'], ['NP\NP']).

en:cat(j0046,[], ['(S\NP)/NP']).
en:cat(j0047,[], ['(S\NP)/NP']).
en:cat(j0048,[], ['(S\NP)/NP']).
en:cat(j0049,[], ['(S\NP)/NP']).
en:cat(j0050,[], ['(S\NP)/NP']).

% --- 文レベルの例外規定 ---
ja:cat(j0051,['ただし'], ['S\(S\NP)']).

en:cat(j0051,[';', provided, however, that], ['(S\NP)/NP']).

ja:cat(j0052,['、'], ['(NP\NP)/NP']).
ja:cat(j0053,['等'], ['(NP\NP)/NP']).
ja:cat(j0054,['又'], ['(NP\NP)/NP']).
ja:cat(j0055,['又は'], ['(NP\NP)/NP']).
ja:cat(j0056,['並びに'], ['(NP\NP)/NP']).

en:cat(j0052,[','], ['(S\NP)/NP']).
en:cat(j0053,[',', 'etc.'], ['(S\NP)/NP']).
en:cat(j0054,[or], ['(S\NP)/NP']).
en:cat(j0055,[or], ['(S\NP)/NP']).
en:cat(j0056,[and], ['(S\NP)/NP']).

ja:cat(j0057,['当分の間'], ['NP/NP']).
ja:cat(j0058,['なおその効力を有する'], ['NP/NP']).
ja:cat(j0059,['みだりに'], ['NP/NP']).

en:cat(j0057,[], ['(S\NP)/NP']).
en:cat(j0058,[], ['(S\NP)/NP']).
en:cat(j0059,[], ['(S\NP)/NP']).

ja:cat(j0060,['同様とする'], ['NP\NP']).
ja:cat(j0061,['とする'], ['NP\NP']).   % 既存
ja:cat(j0062,['みなす'], ['NP\NP']).

en:cat(j0060,[], ['(S\NP)/NP']).
en:cat(j0061,[], ['(S\NP)/NP']).
en:cat(j0062,[], ['(S\NP)/NP']).

ja:cat(j1004,['において準用する',_,'の規定'], ['NP/NP',_,['NP\NP','NP/NP']]).
ja:cat(j1005,['については、',_,'の例による'], ['NP/NP',_,'NP']).
ja:cat(j1006,['の規定は、',_,'について準用する'], [['NP/NP','NP\NP'],_,['NP\NP','NP/NP']]).
ja:cat(j1007,['の規定に違反して',_,'した者'], [['NP/NP','NP\NP'],_,'NP']).
ja:cat(j1008,['の日の',_,'日前までに'], [['NP\NP','NP/NP'],_,'NP']).
ja:cat(j1009,['は、',_,'と解釈してはならない'], ['NP/NP',_,'NP/NP']).
ja:cat(j1034,['の規定は、',_,'についても適用する'],[['NP/NP','NP\NP'],_,['NP\NP','NP/NP']]).
ja:cat(j1038,['は、',_,'と認めるときは'],[f'NP/NP',_,'NP/NP']).

en:cat(j1004,[], ['(S\NP)/NP']).
en:cat(j1005,[], ['(S\NP)/NP']).
en:cat(j1006,[], ['(S\NP)/NP']).
en:cat(j1007,[], ['(S\NP)/NP']).
en:cat(j1008,[], ['(S\NP)/NP']).
en:cat(j1009,[], ['(S\NP)/NP']).

ja:cat(j1010,['なおその効力を有する'],[fun()]).
ja:cat(j1013,['において準用する場合を含む'],[['NP/NP','NP\NP']]).
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
ja:cat(j1025,['については、なお従前の例による'],[fun()]).
ja:cat(j1026,['に照らし'],[fun()]).
ja:cat(j1027,['に満たない'],[fun()]).
ja:cat(j1028,['に基づく'],[fun()]).
ja:cat(j1029,['のいずれかに該当する'],[fun()]).
ja:cat(j1031,['の規定にかかわらず'],[fun()]).
ja:cat(j1032,['の規定により'],[fun()]).
ja:cat(j1036,['の日の翌日から起算して'],[fun()]).
ja:cat(j1039,['は、他の法律に特別の定めのある場合を除くほか、この法律の定めるところによる'],[fun()]).
ja:cat(j1040,['不服を申し立てることができない'],[fun()]).
ja:cat(j1041,['別段の定めがある場合を除き'],[fun()]).
ja:cat(j1042,['別に法律で定める日'],[fun()]).

en:cat(j1010,[], ['(S\NP)/NP']).
en:cat(j1011,[], ['(S\NP)/NP']).
en:cat(j1012,[], ['(S\NP)/NP']).
en:cat(j1013,[], ['(S\NP)/NP']).
en:cat(j1014,[], ['(S\NP)/NP']).
en:cat(j1015,[], ['(S\NP)/NP']).
en:cat(j1016,[], ['(S\NP)/NP']).
en:cat(j1017,[], ['(S\NP)/NP']).
en:cat(j1018,[], ['(S\NP)/NP']).
en:cat(j1019,[], ['(S\NP)/NP']).
en:cat(j1020,[], ['(S\NP)/NP']).
en:cat(j1021,[], ['(S\NP)/NP']).
en:cat(j1022,[], ['(S\NP)/NP']).
en:cat(j1023,[], ['(S\NP)/NP']).
en:cat(j1024,[], ['(S\NP)/NP']).
en:cat(j1025,[], ['(S\NP)/NP']).
en:cat(j1026,[], ['(S\NP)/NP']).
en:cat(j1027,[], ['(S\NP)/NP']).
en:cat(j1028,[], ['(S\NP)/NP']).
en:cat(j1029,[], ['(S\NP)/NP']).
en:cat(j1030,[], ['(S\NP)/NP']).
en:cat(j1031,[], ['(S\NP)/NP']).
en:cat(j1032,[], ['(S\NP)/NP']).
en:cat(j1033,[], ['(S\NP)/NP']).
en:cat(j1034,[], ['(S\NP)/NP']).
en:cat(j1035,[], ['(S\NP)/NP']).
en:cat(j1036,[], ['(S\NP)/NP']).
en:cat(j1037,[], ['(S\NP)/NP']).
en:cat(j1038,[], ['(S\NP)/NP']).
en:cat(j1039,[], ['(S\NP)/NP']).
en:cat(j1040,[], ['(S\NP)/NP']).
