module Util.MorphAnalysis where

import Core.Cat
import Core.Reduce

data Morph = Morph
  { mSurface :: String,
    mPos :: String,
    mLemma :: String
  }
  deriving (Show)

analyze :: String -> IO [Morph]
analyze txt = do
  -- TODO: ここに形態素解析を入れる
  -- 今はダミーで1語だけ返す
  return [Morph txt "名詞" txt]
