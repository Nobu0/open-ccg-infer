module Core.Reduce where

import Core.Cat
import Control.Applicative ((<|>))
import Debug.Trace (trace, traceIO, traceShowId)

-- Forward Composition: (X/Y) (Y/Z) → X/Z
forwardCompose :: Cat -> Cat -> Maybe Cat
forwardCompose (Fun x Fwd y) (Fun y' Fwd z)
  | y == y' = Just (Fun x Fwd z)
forwardCompose _ _ = Nothing

reduceOnce :: [Cat] -> Maybe [Cat]
reduceOnce [] = Nothing
reduceOnce [_] = Nothing
reduceOnce (c1:c2:rest) =
  case tryReduce c1 c2 of
    Just r  -> Just (r : rest)
    Nothing -> do
      rest' <- reduceOnce (c2:rest)
      return (c1 : rest')
{-
reduceOnce :: [Cat] -> Maybe [Cat]
reduceOnce [] = Nothing
reduceOnce [_] = Nothing
reduceOnce (c1 : c2 : rest) =
  case tryReduce c1 c2 of
    Just r -> Just (r : rest)
    Nothing -> do
      rest' <- reduceOnce (c2 : rest)
      return (c1 : rest')
-}

postApp :: Cat -> Cat -> Maybe Cat
postApp x (Fun a Fwd b)
  | a == b && b == x = Just x   -- X  (X/X) → X
postApp _ _ = Nothing

{-
tryReduce :: Cat -> Cat -> Maybe Cat
tryReduce c1 c2 =
      dbg "FC"  (forwardCompose c1 c2)
  <|> dbg "FA"  (forwardApp c1 c2)
  <|> dbg "BA"  (backwardApp c1 c2)
  <|> dbg "SP"  (combineSP c1 c2)
  <|> dbg "PA"  (postApp c1 c2)
-}
dbg :: String -> Maybe Cat -> Maybe Cat
dbg tag r =
  case r of
    Just _  -> trace ("[" ++ tag ++ "] fired") r
    Nothing -> r


tryReduce :: Cat -> Cat -> Maybe Cat
tryReduce c1 c2 =
      forwardCompose c1 c2
  <|> forwardApp c1 c2
  <|> backwardApp c1 c2
  <|> combineSP c1 c2
  <|> postApp c1 c2

reduceAll :: [Cat] -> Maybe Cat
reduceAll cats =
  case reduceOnce cats of
    Nothing ->
      if length cats == 1
        then Just (head cats)
        else Nothing
    Just cats' -> reduceAll cats'

-- 主語述語の最終結合
combineSP :: Cat -> Cat -> Maybe Cat
combineSP (Fun (Atom S) Fwd (Atom NP)) (Fun (Atom S) Bwd (Atom NP)) =
  Just (Atom S)
combineSP _ _ = Nothing

forwardApp :: Cat -> Cat -> Maybe Cat
forwardApp (Fun a Fwd b) x
  | b == x = Just a
forwardApp _ _ = Nothing

backwardApp :: Cat -> Cat -> Maybe Cat
backwardApp x (Fun a Bwd b)
  | b == x = Just a
backwardApp _ _ = Nothing

applyFB :: Cat -> Cat -> [Cat]
applyFB c1 c2 =
  case forwardApp c1 c2 of
    Just r -> [r]
    Nothing ->
      case backwardApp c1 c2 of
        Just r -> [r]
        Nothing -> []
