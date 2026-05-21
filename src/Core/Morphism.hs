module Core.Morphism where

import Core.Cat

data Morphism = Morphism
  { surface :: String,
    cat :: Cat,
    sem :: Lambda,
    weight :: Double
  }

data Token = Token
  { tokSurface :: String,
    tokPos :: String
  }
  deriving (Show)
