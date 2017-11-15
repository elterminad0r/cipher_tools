import Data.List

main = do
    src <- getContents
    putStrLn . concat . transpose . map (concat . words) . lines $ src
