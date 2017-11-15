import sys

if __name__ == "__main__":
    if sys.stdin.isatty():
        sys.exit("This is a command-line script requiring stdin")
    print("".join(map("".join, zip(*map(str.split, sys.stdin)))))
