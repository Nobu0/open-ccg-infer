:- use_module(library(process)).

get_unique_prefs :-
    get_parsed_data.

% 1. メインの入り口（結果をリストとして戻さず、この中で完結させる）
get_parsed_data :-
    SQL = "SELECT DISTINCT class_id, box_type FROM box_tbl WHERE class_id < 899 AND lang=2 ORDER BY class_id, box_type;",
    DBPath = 'C:/Users/blue3/haskell/ccg-infer/db/ccgDB.sqlite',
    
    OutputPath = 'C:/Users/blue3/haskell/ccg-infer/poslist.txt',
    tell(OutputPath),
    
    process_create(path(sqlite3), [DBPath, SQL], [stdout(pipe(Output))]),
    
    % 安全弁のリストを持たせず、純粋にストリームを最後まで回す
    read_and_process_stream(Output),
    close(Output),
    
    told,
    format('--- [DONE] Results written to ~w ---~n', [OutputPath]).

% 2. 1行読み込むループ（エラーが起きても絶対に途中で止まらないガード付き）
read_and_process_stream(Stream) :-
    read_line_to_codes(Stream, Codes),
    (   Codes == end_of_file
    ->  writeln('%--- [SUCCESS] End of File reached normally ---')
    ;   string_codes(LineString, Codes),
        (   LineString == ""
        ->  read_and_process_stream(Stream)
        ;   % catch/3 を使い、パース処理でどんなエラーや失敗が起きても
            % プログラムを絶対に終了させず、強制的に次の行へ進める（例外処理）
            catch(
                (   parse_line(LineString, ID, ListOut)
                ->  format('clsid:pos(~w, ~p).~n', [ID, ListOut])
                ;   % パース自体が failure（失敗）した場合はここを通る
                    % 画面（ファイル）に警告を残して次へ
                    format('/* [PARSE FAILED] Line: ~w */~n', [LineString])
                ),
                Error,
                % 万が一システムエラー（インデックス範囲外など）が起きてもここを通り次へ
                format('/* [PARSE ERROR: ~w] Line: ~w */~n', [Error, LineString])
            ),
            % ★何があっても必ず次の行の読み込みに移行する
            read_and_process_stream(Stream)
        )
    ).


% 履歴リストを直近100件に制限してメモリパンクを防ぐ補助述語
update_seen_ids(ID, SeenIDs, [ID | Trimmed]) :-
    (   length(SeenIDs, Len), Len >= 100
    ->  append(Trimmed, [_], SeenIDs) % 末尾の古い1件を削る
    ;   Trimmed = SeenIDs
    ).




% 1. メインの入り口（一時保存用の空リスト [] を渡して開始する）
read_and_parse_lines(Stream, FinalResults) :-
    % 空のリストからスタートし、逆順で溜まった結果を最後に反転（reverse）させて完成させる
    read_and_parse_lines_loop(Stream, [], ReversedResults),
    reverse(ReversedResults, FinalResults).

% 2. 実際にループする内部述語（末尾再帰最適化）
read_and_parse_lines_loop(Stream, Acc, FinalResults) :-
    read_line_to_codes(Stream, Codes),
    (   Codes == end_of_file
    ->  % ファイルが終わったら、溜まったデータを最終結果に代入して終了！
        FinalResults = Acc
    ;   string_codes(LineString, Codes),
        (   LineString == ""
        ->  % 空行なら、そのまま次のループへ（メモリは消費しない）
            read_and_parse_lines_loop(Stream, Acc, FinalResults)
        ;   (   parse_line(LineString, ID, ListOut)
            ->  % パースに成功したら、Acc の先頭にデータを追加して次のループへ（メモリ消費ゼロ！）
                NewAcc = [data(ID, ListOut) | Acc],
                read_and_parse_lines_loop(Stream, NewAcc, FinalResults)
            ;   % パースに失敗した場合も、そのまま次のループへ
                read_and_parse_lines_loop(Stream, Acc, FinalResults)
            )
        )
    ).


% 2. 1行の文字列を「ID」と「テキスト部分」に分割する
parse_line(LineString, ID, ListOut) :-
  parse_line2(LineString, ID2, ListOut2),
  atom_number(ID2,ID),
  (ID<210 -> append(ListOut,[_],ListOut2)
  ;ID<310 -> ListOut = ListOut2
  ;append(ListOut,[_],ListOut2)
  ).

parse_line2(LineString, ID, ListOut) :-
    split_string(LineString, "|", "", [IDStr, TextStr | _Rest]),
    atom_string(ID, IDStr),
    TextStr \== "",
    (   sub_string(TextStr, 0, 1, _, "(")
    ->  parse_bracket_format(TextStr, ListOut)
    ;   parse_space_format(TextStr, ListOut)
    ).

% 3. フォーマット1の処理（安全版）
parse_bracket_format(TextStr, List) :-
    string_length(TextStr, Len),
    Len > 2,
    InnerLen is Len - 2,
    sub_string(TextStr, 1, InnerLen, _, InnerStr),
    split_string(InnerStr, ",", " '", RawStrList),
    exclude([S]>>(S==""; S==" "), RawStrList, CleanStrList),
    maplist(atom_string, List, CleanStrList).

% 4. フォーマット2の処理（安全版）
parse_space_format(TextStr, List) :-
    split_string(TextStr, " ", " ", RawStrList),
    exclude([S]>>(S==""; S==" "), RawStrList, CleanStrList),
    maplist(atom_string, List, CleanStrList).
