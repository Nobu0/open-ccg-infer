module Lang.English.MorphAnalysis where

import Util.Morph (Morph (..))

analyze :: String -> IO [Morph]
analyze txt = return $ map lineToMorph (lines txt)

lineToMorph :: String -> Morph
lineToMorph line =
  case words line of
    (_ : _ : _ : _ : _ : _ : surf : pos : _) ->
      Morph surf pos surf
    _ ->
      Morph "" "" ""
