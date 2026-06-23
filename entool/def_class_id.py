PAT_CLASS = {
    101: {'typ':'#ADDR_ART', 'nam':'条（Article）'},
    102: {'typ':'#ADDR_PAR', 'nam':'項（Paragraph）'},
    103: {'typ':'#ADDR_NUM', 'nam':'号（Item Number）'},
    104: {'typ':'#ADDR_PAT', 'nam':'編（Part）'},
    105: {'typ':'#ADDR_CHA', 'nam':'章（Chapter）'},
    106: {'typ':'#ADDR_SEC', 'nam':'節（Section）'},
    107: {'typ':'#ADDR_SUB', 'nam':'款（Subsection）'},
    108: {'typ':'#ADDR_DIV', 'nam':'目（Division）'},

    201: {'typ':'#FIXED_PP',  'nam':'英語の固定前置詞句'},
    202: {'typ':'#FIXED_INF', 'nam':'英語の不定詞句'},

    301: {'typ':'', 'nam':"名詞句 (SIMPLE)"},
    302: {'typ':'', 'nam':"名詞句（REL）"},
    303: {'typ':'', 'nam':"アドレスを含む名詞句、数詞を含む(ADDR)"},
    304: {'typ':'', 'nam':"法令での名詞句等(OTHER)"},
    305: {'typ':'', 'nam':"その他の名詞句等(REFER)"},

    401: {'typ':'#CCG_LEFT',  'nam':'CCG 左結合（A/B + B → A）'},
    402: {'typ':'#CCG_RIGHT', 'nam':'CCG 右結合（B + B\\A → A）'},
    403: {'typ':'#VP',        'nam':'動詞句（Verb Phrase）'},

    501: {'typ':'#PP',     'nam':'前置詞句（英語）'},
    502: {'typ':'#ADV',    'nam':'副詞句'},
    503: {'typ':'#CLAUSE', 'nam':'節（S/NP, S\\NP など）'},

    # --- 900番台：構造句（STRUCT） ---
    900: {'typ':'#STRUCT', 'nam':'構造句（構造的要素の親カテゴリ）'},
    # 括弧BOX（最重要）
    901: {'typ':'#PAREN',  'nam':'括弧句（括弧で囲まれた部分を丸ごとBOX化）'},
    # 条番号・項番号（Article 3, paragraph (1) など）
    902: {'typ':'#REF',    'nam':'参照句（Article/Section/paragraph/item）'},
    # 範囲表現（from X to Y / between X and Y）
    903: {'typ':'#RANGE',  'nam':'範囲句（from X to Y / between X and Y）'},
    # 数値＋単位（30 days / 12 months）
    904: {'typ':'#NUMUNIT','nam':'数量句（数値＋単位）'},
    # 注釈・補足（if any / as appropriate）
    905: {'typ':'#NOTE',   'nam':'注釈句（補足情報）'},
}
