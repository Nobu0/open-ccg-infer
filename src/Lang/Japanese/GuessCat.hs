module Lang.Japanese.GuessCat where

import Core.Cat
import Core.Morphism
import Lang.Japanese.Dictionary
import Util.Loader
import Util.MorphAnalysis
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
  | surf == "が" = Fun (Atom S) Fwd (Atom NP)
  | surf == "を" = Fun (Atom NP) Bwd (Atom NP)
  | pos == "名詞" = Atom NP
  | pos == "動詞" = Fun (Atom S) Bwd (Atom NP)
  | otherwise = Atom NP

{-
tokenToMorphism :: Token -> IO Morphism
tokenToMorphism (Token surf posTag) = do
  c <- guessCat posTag surf
  return
    Morphism
      { surface = surf,
        cat = c,
        sem = LVar surf,
        weight = 1.0
      }

guessCatJp :: String -> String -> IO Cat
guessCatJp posTag surf
  | posTag == "名詞" = do
      sahen <- isSahen surf
      if sahen
        then return (Fun (Fun (Atom S) Bwd (Atom NP)) Bwd (Atom NP))
        else return (Atom NP)
  -- 動詞「する」など
  | posTag == "動詞" =
      return (Fun (Fun (Atom S) Bwd (Atom NP)) Bwd (Atom NP))
  -- が
  -- が : (S/NP)\NP
  | surf == "が" =
      return (Fun (Fun (Atom S) Fwd (Atom NP)) Bwd (Atom NP))
  | surf == "を" =
      return (Fun (Atom NP) Bwd (Atom NP))
  | posTag == "助詞" && surf == "を" =
      return (Fun (Fun (Atom S) Bwd (Atom NP)) Fwd (Fun (Atom S) Bwd (Atom NP)))
  | posTag == "助詞" && surf == "が" =
      return (Fun (Atom S) Bwd (Fun (Atom S) Fwd (Atom NP)))
  | posTag == "助詞" =
      return (Atom PP)
  | otherwise =
      return (Atom NP)
-}
