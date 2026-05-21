module Core.Reduce where

import Core.Cat

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
