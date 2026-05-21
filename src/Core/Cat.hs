module Core.Cat where

-- deriving (Eq, Show)

-- 基本カテゴリ（原子カテゴリ）
data BaseCat
  = S -- 文
  | NP -- 名詞句
  | N -- 名詞
  | PP -- 前置詞句（日本語では格助詞相当）
  | CONJ -- 接続詞
  deriving (Eq, Show)

-- スラッシュ方向
data Dir = Fwd | Bwd
  deriving (Eq, Show)

-- CCG カテゴリ（再帰的）
data Cat
  = Atom BaseCat
  | Fun Cat Dir Cat -- A/B または A\B
  deriving (Eq, Show)

-- 意味論（λ項）
data Lambda
  = LVar String
  | LApp Lambda Lambda
  | LAbs String Lambda
  deriving (Eq, Show)
