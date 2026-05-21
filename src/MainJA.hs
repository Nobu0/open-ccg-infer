module Main where

import CCG
import Morph

main :: IO ()
main = do
  let tokens =
        [ Token "我が国" "名詞",
          Token "が" "助詞",
          Token "条約" "名詞",
          Token "を" "助詞",
          Token "遵守" "名詞",
          Token "する" "動詞"
        ]

  -- IO Morphism をまとめて実行
  morphs <- mapM tokenToMorphism tokens

  putStrLn "Morphisms:"
  mapM_ print morphs

  let cats = map cat morphs
  print cats
  print (reduceOnce cats)
  print (reduceAll cats)

{-
  putStrLn "\nCats:"
  mapM_ print cats

  putStrLn "\nTry F/B on last two:"
  case reverse cats of
    (c2 : c1 : _) -> print (applyFB c1 c2)
    _ -> putStrLn "not enough cats"
-}