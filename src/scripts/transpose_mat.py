import sys

print("".join(map("".join, zip(*map(str.split, sys.stdin)))))
