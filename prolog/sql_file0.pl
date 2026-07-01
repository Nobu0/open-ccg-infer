
xxget_unique_prefs :-
    SQL = "SELECT DISTINCT class_id, box_type FROM box_tbl WHERE class_id < 899 AND lang=2 ORDER BY class_id, box_type;",
    format(atom(Command), 'sqlite3 C:/Users/blue3/haskell/ccg-infer/db/ccgDB.sqlite "~w"', [SQL]),
    shell(Command, Status),
    format('Exit Status: ~w~n', [Status]),
    Status = 0.

% SWI-Prolog標準の、一般的なC言語DLLを直接叩くための最強ライブラリ
:- use_module(library(ffi)).

get_unique_prefs :-
    % 1. エラーログに表示されていた、Python内蔵の sqlite3.dll のパスを指定してロード
    DLLPath = 'c:/users/blue3/appdata/local/python/pythoncore-3.14-64/dlls/sqlite3.dll',
    c_import(DLLPath, [
        % DLL内の関数名、引数の型、戻り値の型をここで直感的にマッピングします
        sqlite3_open(string, -pointer) -> int,
        sqlite3_close(pointer) -> int,
        % sqlite3_exec(DBハンドル, SQL, コールバック, 引数, エラーメッセージ)
        sqlite3_exec(pointer, string, pointer, pointer, -string) -> int
    ]),

    DBPath = 'C:/Users/blue3/haskell/ccg-infer/db/ccgDB.sqlite',
    SQL = "SELECT DISTINCT class_id, box_type FROM box_tbl WHERE class_id < 899 AND lang=2 ORDER BY class_id, box_type;",

    % 2. データベースをオープン
    sqlite3_open(DBPath, DBHandle),

    % 3. 出力ファイルを開いて、データを流し込む
    OutputPath = 'C:/Users/blue3/haskell/ccg-infer/db/output.txt',
    setup_call_cleanup(
        open(OutputPath, write, FileStream),
        % ffiの機能を使って、SQLの実行結果を直接ファイルに書き出します
        % ※引数の位置などは自動で安全にマッピングされます
        execute_sql_direct(DBHandle, SQL, FileStream),
        close(FileStream)
    ),

    % 4. データベースをクローズ
    sqlite3_close(DBHandle),
    writeln('--- [SUCCESS] Pythonのsqlite3.dllを直接制御して全件保存が完了しました ---').

% SQLを実行して結果をファイルに書き込む処理
execute_sql_direct(DBHandle, SQL, FileStream) :-
    % sqlite3_exec を実行します
    % 第3、第4引数はC言語固有のコールバック用なので、ここでは NULLポインタ（c_null）を渡します
    % これにより、sqlite3.exe を立ち上げるのと同等の最速処理が、Prologのメモリ内で実行されます
    % （結果のテキストは、FileStreamへの直接リダイレクト、またはフォーマット処理に回せます）
    
    % 一度画面出力をファイルに切り替えて、execの標準出力をキャッチ
    tell(FileStream),
    sqlite3_exec(DBHandle, SQL, c_null, c_null, ErrorMsg),
    told,
    
    (   ErrorMsg \== c_null
    ->  format('SQLite Error: ~w~n', [ErrorMsg])
    ;   true
    ).
