{-
module Main where

import Core.Reduce
import Lang.Japanese.GuessCat -- ← 日本語版
-- import Lang.English.GuessCat -- ← 英語版に切り替えるだけ
import Util.MorphAnalysis

main :: IO ()
main = do
  text <- getLine
  morphs <- analyze text
  let cats = map guessCat morphs
  print (reduceAll cats)

module Main where

import Core.Morphism (Morphism (..))
import Core.Reduce (reduceAll)
-- import Lang.Japanese.GuessCat (guessCat)
import Lang.English.GuessCat (guessCat)
import Lang.English.MorphAnalysis (analyze)

main :: IO ()
main = do
  text <- getLine
  morphs <- analyze text
  let morphisms = map guessCat morphs
  let cats = map cat morphisms
  print (reduceAll cats)
-}

module Main where

import Control.Monad (guard)
import Core.Morphism (Morphism (..))
import Core.Reduce (reduceAll)
import Lang.English.GuessCat (guessCat)
import Lang.English.MorphAnalysis (analyze)
import System.Environment (getArgs)

{-
main :: IO ()
main = do
  args <- getArgs
  case args of
    [fileName] -> do
      txt <- readFile fileName
      morphs <- analyze txt
      let morphisms = map guessCat morphs
      let cats = map cat morphisms
      print (reduceAll cats)
    _ -> putStrLn "Usage: ccg-infer <filename>"
-}

main :: IO ()
main = do
  args <- getArgs
  case args of
    [fileName] -> do
      txt <- readFile fileName
      morphs <- analyze txt

      -- 各語について複数 Morphism を生成
      let morphismOptions :: [[Morphism]]
          morphismOptions = map guessCat morphs

      -- 全組み合わせ生成
      let allPatterns :: [[Morphism]]
          allPatterns = sequence morphismOptions

      -- S になるパターンだけ残す
      let validPatterns =
            [ p
            | p <- allPatterns,
              reduceAll (map cat p) == Just (Atom S)
            ]

      print validPatterns
    _ -> putStrLn "Usage: ccg-infer <filename>"
