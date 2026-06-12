# ccg-infer

## 目的（Purpose）

このプロジェクトの目的は、
法令文の構造をできるだけ機械的・自動的に抽出し、
日英で共通の構文表現に落とし込むための仕組みを作ること  
にあります。

## 概要（Overview）

このプロジェクトは、
日本語および英語の法令文を対象に、
句レベルの構造（phrase structure）を自動的に抽出し、
CCG（Combinatory Categorial Grammar）形式の構文木として可視化する  
ことを目的とした個人研究です。

法令文は一般的な文とは異なり、
述語中心の文構造（S）よりも 名詞句（NP）の連鎖 によって意味が形成されます。
そのため本プロジェクトでは、文全体を NP 主体の構造 として扱い、
句の結合関係を CCG の関数型カテゴリ（例：NP/NP, PP/NP）で表現します。

主な特徴（Key Features）

## 1. NX-gram 法による構文テンプレートの自動抽出

独自の NX-gram 法 を用いて、
大量の法令文から 品詞パターン → テキスト N-gram の二段階で
構造的に意味のあるフレーズを自動抽出します。

この手法により、英語では以下のような固定句が自動的に検出されます：

in accordance with

in violation of

in connection with

on behalf of

with jurisdiction over

これらは PP/NP（右側の NP を取る関数） として扱われ、
日本語の「NP/NP（の）」と同じ役割を果たします。

## 2. 日本語・英語の BOX 化（構文単位化）

抽出したフレーズを BOX（構文単位） として分類し、
SQLite データベースに格納します。

BOX は以下のようなカテゴリに分類されます：

NP（名詞句）

NP/NP（連体修飾）

PP/NP（前置詞句）

固定句（MWE）

アドレス（section 12, 第3項 など）

## 3. CCG による構文木生成

BOX を入力として、
apply_ccg アルゴリズムにより句同士を結合し、
最終的に CCG 構文木（Graphviz PNG） を生成します。

これにより、
日本語と英語の法令文を 同じ構造形式で比較 できます。

# クラスIDの説明

## ３００番台は、英語の名詞句（NP）

３００番台は、名詞句を CCG の NP カテゴリにマッピングする前段階の「構造分類」。

CCG の NP は本来 単一カテゴリですが、
実際の法令文では NP の内部構造が非常に多様で、
そのまま NP として扱うと 構文木が爆発する。

そこで NP を次のように分割している：

BOX 内容 CCGでの扱い
301 一般NP（名詞句） NP
302 関係節を含むNP（NP_REL） NP（内部に S/NP を含む）
303 固定句NP（FIXED_NP） NP（辞書的NP）
304 その他NP（一般NPの残り） NP
305 特殊NP（固有名詞連結など） NP

つまり：

300番台はすべて最終的には CCG の NP に収束するが、
その内部構造の違いを BOX で事前に整理している。

これは 英語法令文の構文解析では必須の工夫です。

## CCG の観点から見た 300番台の役割

### ① CCG は NP の内部構造を区別しない（理論上）

CCG の辞書では：

“the man” → NP

“the man who left” → NP

“the purpose of this Act” → NP

“United Nations General Assembly” → NP

すべて 同じ NP。

しかし、法令文ではこれが破綻する。

### ② 法令文の NP は内部構造が複雑すぎる

コーパスでは：

固有名詞連結（NNP NNP NNP）

関係節（who, which, that）

前置詞句（of, for, under）

固定句（in accordance with）

特殊アドレス句（Part IVA, Section 27‑bis）

これらが大量に出現する。

そのため：

NP の内部構造を BOX で分類しないと、
CCG の構文木が指数爆発する。

### ③ 300番台は CCG の “辞書カテゴリ” を安定化させるための前処理

CCG の辞書は本来：

名詞 → NP

名詞句 → NP

固有名詞 → NP

関係節 → (NP\NP)/(S/NP)

しかし、法令文ではこれでは不十分。

そこで 300番台が必要になる：

301：普通の NP

302：関係節を含む NP

303：固定句 NP

304：一般NPの残り

305：固有名詞連結など特殊NP

これにより：

CCG の辞書カテゴリが安定し、構文木が破綻しない。

## 300番台と CCG の “直接対応表”

BOX NPの内部構造 CCGカテゴリ 説明
301 普通の名詞句 NP the purpose, the Act
302 関係節を含むNP NP（内部に S/NP） the man who left
303 固定句NP NP（辞書的） in accordance with the Act
304 その他の一般NP NP paragraph, item, provision
305 固有名詞連結・特殊NP NP United Nations General Assembly

すべて最終的には NP だが、
内部構造が違うため BOX で分けている。

## なぜ英語で 300番台が特に重要なのか？

英語法令文は：

固有名詞連結が多い

関係節が多い

前置詞句が多い

固定句が多い

アドレス句が特殊（Part IVA, Section 27‑bis）

つまり：

英語の NP は日本語よりも “内部構造の種類” が多い。

そのため：

301〜305 の分類は 英語でこそ必要

CCG の NP を安定化させるための “必須の前処理” になる
