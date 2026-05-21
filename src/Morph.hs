module Morph where

import CCG
import Dbinf

data Token = Token
  { tokSurface :: String,
    tokPos :: String
  }
  deriving (Show)

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

reduceOnce :: [Cat] -> Maybe [Cat]
reduceOnce (c1 : c2 : rest) =
  case forwardApp c1 c2 of
    Just r -> Just (r : rest)
    Nothing ->
      case backwardApp c1 c2 of
        Just r -> Just (r : rest)
        Nothing ->
          case combineSP c1 c2 of
            Just r -> Just (r : rest)
            Nothing -> do
              rest' <- reduceOnce (c2 : rest)
              return (c1 : rest')
reduceOnce _ = Nothing

reduceAll :: [Cat] -> [Cat]
reduceAll [c] = [c]
reduceAll (Atom S : _) = [Atom S] -- ★ ここを追加
reduceAll cs =
  case reduceOnce cs of
    Just cs' -> reduceAll cs'
    Nothing -> cs

-- 主語述語の最終結合
combineSP :: Cat -> Cat -> Maybe Cat
combineSP (Fun (Atom S) Fwd (Atom NP)) (Fun (Atom S) Bwd (Atom NP)) =
  Just (Atom S)
combineSP _ _ = Nothing

guessCat :: String -> String -> IO Cat
guessCat posTag surf
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
