"""
Show information about where perturbations happen in given clusters
"""

import argparse

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=argparse.FileType("r"), help="input file")
    return parser.parse_args()

def inform(row):
    words = [node.split("_")[0] for node in row.split()]
    perts = [ind for ind, row in enumerate(zip(*words)) if len(set(row)) != 1]
    return "{{{}}}: {}".format(" ".join(map(str, perts)), " ".join(sorted(row.split(), key=lambda x: int(x.split("_")[1]))))

if __name__ == "__main__":
    args = get_args()
    for line in args.input:
        print(inform(line))
