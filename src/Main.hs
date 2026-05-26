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
import Core.Cat
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

      let morphismOptions :: [[Morphism]]
          morphismOptions = map guessCat morphs

      let allPatterns :: [[Morphism]]
          allPatterns = sequence morphismOptions

      let validPatterns =
            [ p
            | p <- allPatterns,
              reduceAll (map cat p) == Just (Atom S)
            ]

      putStrLn "=== ALL PATTERNS ==="
      mapM_ (print . map cat) allPatterns

      putStrLn "=== REDUCE RESULTS ==="
      mapM_ (\p -> print (map cat p, reduceAll (map cat p))) allPatterns

      putStrLn "=== VALID PATTERNS ==="
      mapM_ print
        [ reduceAll (map cat p)
        | p <- allPatterns
        , reduceAll (map cat p) == Just (Atom S)
        ]
      putStrLn "=== VALID DISCRIPTION PATTERNS ==="
      mapM_ print
        [ (map cat p, reduceAll (map cat p))
        | p <- allPatterns
        , reduceAll (map cat p) == Just (Atom S)
        ]

    _ -> putStrLn "Usage: ccg-infer <filename>"

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
