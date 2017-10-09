import sys
import re
pat = re.compile(r"(?<=\")[^\"]*\.html")
print("\n".join(pat.findall(sys.stdin.read())))
