{-
module Lang.English.GuessCat where

import Core.Cat
import Core.Morphism
import Util.MorphAnalysis (Morph (..))

guessCat :: Morph -> Morphism
guessCat (Morph surf pos lemma) =
  Morphism
    { surface = surf,
      cat = guessCatCore pos surf,
      sem = LVar surf,
      weight = 1.0
    }

guessCatCore :: String -> String -> Cat
guessCatCore pos surf
  | pos == "NOUN" = Atom NP
  | pos == "VERB" = Fun (Fun (Atom S) Bwd (Atom NP)) Fwd (Atom NP) -- 他動詞: (S\NP)/NP
  | pos == "ADJ" = Fun (Atom N) Fwd (Atom N) -- 形容詞: N/N
  | pos == "ADV" = Fun v Bwd v -- 副詞: (S\NP)\(S\NP)
  | otherwise = Atom NP
  where
    v = Fun (Atom S) Bwd (Atom NP) -- S\NP
-}
module Lang.English.GuessCat where

import Core.Cat
import Core.Morphism
import Util.Morph (Morph (..))

guessCat :: Morph -> [Morphism]
guessCat (Morph surf pos lemma) =
  [ Morphism surf cat (LVar surf) 1.0
  | cat <- guessCatCore pos surf
  ]

{-
guessCat :: Morph -> Morphism
guessCat (Morph surf pos lemma) =
  Morphism
    { surface = surf,
      cat = guessCatCore pos surf,
      sem = LVar surf,
      weight = 1.0
    }
-}

guessCatCore :: String -> String -> [Cat]
guessCatCore pos surf
  | pos == "DT" = [NP `Fwd` N]
  | pos == "NN" = [NP]
  | pos == "IN" = [PP `Fwd` NP, (NP `Bwd` NP) `Fwd` NP] -- with, into など
  | pos == "VB" =
      [ S `Bwd` NP,
        (S `Bwd` NP) `Fwd` PP -- comply のような PP を取る動詞
      ]
  | otherwise = [NP]

allMorphismPatterns :: [[Morphism]] -> [[Morphism]]
allMorphismPatterns = sequence

{-
guessCatCore :: String -> String -> Cat
guessCatCore pos surf
  -- 冠詞
  | pos == "DT" = Fun (Atom NP) Fwd (Atom N) -- NP/N

  -- 名詞
  | pos `elem` ["NN", "NNS", "NNP", "NNPS"] = Atom NP
  -- 形容詞
  | pos == "JJ" = Fun (Atom N) Fwd (Atom N) -- N/N

  -- 自動詞 + PP を取る動詞（comply）
  | surf == "comply" = Fun (Fun (Atom S) Bwd (Atom NP)) Fwd (Atom PP)
  -- 過去分詞 entered（S/NP を取る）
  | pos == "VBN" = Fun (Atom S) Fwd (Atom NP)
  -- 助動詞 shall
  | pos == "MD" =
      let v = Fun (Atom S) Bwd (Atom NP)
       in Fun v Fwd v
  -- 前置詞 with, into
  | pos == "IN" = Fun (Atom PP) Fwd (Atom NP) -- PP/NP

  -- 接続詞 and
  | pos == "CC" =
      let x = Atom NP
       in Fun (Fun x Bwd x) Fwd x -- (X\X)/X

  -- 関係代名詞 which
  | pos == "WDT" =
      Fun (Fun (Atom NP) Bwd (Atom NP)) Fwd (Fun (Atom S) Fwd (Atom NP))
  -- (NP\NP)/(S/NP)

  -- 動詞（一般）
  | pos `elem` ["VB", "VBD", "VBP", "VBZ"] =
      Fun (Atom S) Bwd (Atom NP) -- S\NP

  -- 句読点
  | pos == "." = Atom S
  -- デフォルト
  | otherwise = Atom NP

guessCatCoreOrg :: String -> String -> Cat
guessCatCoreOrg pos surf
  -- 冠詞
  | pos == "DT" = Fun (Atom NP) Fwd (Atom N) -- NP/N
  -- 名詞
  | pos `elem` ["NN", "NNS", "NNP", "NNPS"] = Atom NP
  -- 形容詞
  | pos == "JJ" = Fun (Atom N) Fwd (Atom N) -- N/N
  -- 動詞（とりあえず S\NP としておく）
  | pos `elem` ["VB", "VBD", "VBP", "VBZ", "VBN", "VBG"] =
      Fun (Atom S) Bwd (Atom NP) -- S\NP
      -- 助動詞 shall, will など: (S\NP)/(S\NP)
  | pos == "MD" =
      let v = Fun (Atom S) Bwd (Atom NP)
       in Fun v Fwd v
  -- 前置詞 with, into など: (NP\NP)/NP としておく
  | pos == "IN" =
      Fun (Fun (Atom NP) Bwd (Atom NP)) Fwd (Atom NP)
  -- 接続詞 and: X\X / X とか色々あるが、とりあえず S\S として無害化
  | pos == "CC" = Fun (Atom S) Bwd (Atom S)
  -- 関係代名詞 which: とりあえず NP\NP
  | pos == "WDT" = Fun (Atom NP) Bwd (Atom NP)
  -- 句読点は無視
  | pos == "." = Atom S
  -- デフォルト
  | otherwise = Atom NP
-}
