module CCG where

-- import Data.Text (Text)
instance Show Morphism where
  show (Morphism s c sem w) =
    "Morphism {surface = "
      ++ s
      ++ ", cat = "
      ++ show c
      ++ ", sem = "
      ++ show sem
      ++ ", weight = "
      ++ show w
      ++ "}"

data Morphism = Morphism
  { surface :: String,
    cat :: Cat,
    sem :: Lambda,
    weight :: Double
  }

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

forwardApp :: Cat -> Cat -> Maybe Cat
forwardApp (Fun a Fwd b) x
  | b == x = Just a
forwardApp _ _ = Nothing

backwardApp :: Cat -> Cat -> Maybe Cat
backwardApp x (Fun a Bwd b)
  | b == x = Just a
backwardApp _ _ = Nothing

-- CCG.hs か別モジュールでもOK

applyFB :: Cat -> Cat -> [Cat]
applyFB c1 c2 =
  case forwardApp c1 c2 of
    Just r -> [r]
    Nothing ->
      case backwardApp c1 c2 of
        Just r -> [r]
        Nothing -> []
