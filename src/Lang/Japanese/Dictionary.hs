{-# LANGUAGE OverloadedStrings #-}

module Lang.Japanese.Dictionary where

import qualified Data.Text as T
import Database.SQLite.Simple
import Database.SQLite.Simple.FromRow

isSahen :: String -> IO Bool
isSahen word = do
  conn <- open "db/sahen.sqlite"
  rows <- query conn "SELECT word FROM sah_tbl WHERE word = ?" (Only word) :: IO [Only T.Text]
  close conn
  return (not (null rows))
