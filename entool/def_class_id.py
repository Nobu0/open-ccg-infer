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

##################################################
# 句を範囲を決定する関数
##################################################
def is_main_verb(pos, txt):
    """主節動詞の開始判定"""
    # MD + VB, VB*, BE/HAVE + VBN/VBG などをまとめて扱う
    if pos in ("VB", "VBD", "VBP", "VBZ"):
        return True
    if pos == "MD":
        return True
    if pos in ("VBN", "VBG") and txt not in ("prescribed", "provided", "given", "granted"):
        # provided/prescribed は後置修飾なので除外
        return True
    return False


def is_relation_clause_start(tokens, i):
    """ , which / , who / , where / , when / , that の判定 """
    if tokens[i][1] != ",":
        return False
    if i+1 >= len(tokens):
        return False

    pos, txt = tokens[i+1]

    # 非制限用法の関係節
    if pos in ("WDT", "WP", "WRB"):
        return True
    if txt.lower() == "that":
        return True

    return False


def is_condition_clause_start(tokens, i):
    """ provided, however, that / if / unless / when / where """
    txt = tokens[i][1].lower()

    if txt == "provided":
        # provided, however, that
        return True
    if txt in ("if", "unless", "when", "where"):
        return True

    return False


def is_np_continuation(pos, txt):
    """NP 継続条件（簡略版）"""
    if pos in ("NN", "NNS", "NNP", "NNPS", "DT", "JJ", "JJR", "JJS", "RB", "CD", "PRP$", "POS"):
        return True

    # PP の開始
    if pos == "IN":
        return True

    # 後置修飾（provided/prescribed/given/granted）
    if pos in ("VBN", "VBG") and txt.lower() in ("prescribed", "provided", "given", "granted"):
        return True

    # etc. は NP 内部
    if txt.lower() == "etc.":
        return True

    return False


def extract_np(tokens):
    i = 0
    L = len(tokens)

    while i < L:
        pos, txt = tokens[i]

        # --- 強制終端（法令文専用） ---
        if txt.lower() in ("shall", "may", "must", "can", "will", "should"):
            break

        # --- 通常の終端条件 ---
        if is_main_verb(pos, txt):
            break
        if txt in (".", ";"):
            break
        if is_relation_clause_start(tokens, i):
            break
        if is_condition_clause_start(tokens, i):
            break

        # --- IN の直後の DT/JJ/NN は PP 継続 ---
        if i > 0:
            prev_pos, prev_txt = tokens[i-1]
            if prev_pos == "IN" and pos in ("DT", "JJ", "JJR", "JJS", "NN", "NNS", "NNP", "NNPS"):
                i += 1
                continue

        # --- 単独継続条件 ---
        if is_np_continuation(pos, txt):
            i += 1
            continue

        break

    return tokens[:i]

def find_np_start(tokens, start_i, end_i, dbg=0):
    i = start_i
    lng = len(tokens)

    while i > (start_i - end_i) and i < lng:
        pos, txt = tokens[i]
        if dbg == 1:
            print("i=",i,pos,txt)
        # --- ここで止める条件 ---
        # IN の前には遡らない（NP は IN の直後から始まる）
        # 主節動詞の前には遡らない
        if pos in ("VB", "VBD", "VBP", "VBZ", "MD", "IN", "TO", "CC"):
            break

        # --- 遡ってよい条件 ---
        if pos in ("DT", "JJ", "JJR", "JJS", "RB", "CD",
                    "NN", "NNS", "NNP", "NNPS", "PRP$", "POS"):
            i -= 1
            continue

        break

    return i


def extract_WH_clause(sta, tokens):
    i = 0
    L = len(tokens)

    while i < L:
        pos, txt = tokens[i]

        # 終端条件
        if txt in (",", ";", ".", "(", ")"):
            break
        if pos in ("VB", "VBD", "VBP", "VBZ", "MD"):
            break
        if txt.lower() in ("and", "or"):
            break
        if txt.lower() == "provided":
            break

        i += 1

    return sta + i

