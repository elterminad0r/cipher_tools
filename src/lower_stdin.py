import sys

if __name__ == "__main__":
    if sys.stdin.isatty():
        sys.exit("this is a command line script")
    sys.stdout.write(sys.stdin.read().upper())
