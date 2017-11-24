#!/usr/bin/env python3

"""
Script that eats one line input. This is literally useless unless you're
scripting from sh or you particularly like hitting the enter key
"""

import argparse

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()

if __name__ == "__main__":
    get_args()
    input()
