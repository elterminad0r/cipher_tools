"""
merry christmas
"""

import datetime
import argparse

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("nothing", type=str)
    parser.add_argument("--infinity", action="store_true")
    return parser.parse_args()

xm_form = "{days:02} days, {hours:02} hours, {minutes:02}:{seconds:06.3f}s to go until christmas!"
ot_form = "More importantly,\n{days:02} days, {hours:02} hours, {minutes:02}:{seconds:06.3f}s to go until challenge 8!"

def strfdelta(delta, fstr):
    seconds = int(delta.total_seconds())
    days, rem = divmod(seconds, 60 ** 2 * 24)
    hours, rem = divmod(rem, 60 ** 2)
    minutes, rem = divmod(rem, 60)
    seconds = delta.total_seconds() % 60
    return fstr.format(**locals())

if __name__ == "__main__":
    args = get_args()
    if not args.infinity:
        nw = datetime.datetime.now()
        remaining = (datetime.datetime(year=2017, month=12, day=14, hour=15) - nw)
        xmr = (datetime.datetime(year=2017, month=12, day=25, hour=0) - nw)
        print("{}\n{}".format(strfdelta(xmr, xm_form), strfdelta(remaining, ot_form)))
    else:
        while True:
            nw = datetime.datetime.now()
            remaining = (datetime.datetime(year=2017, month=12, day=14, hour=15) - nw)
            print("\r{}".format(strfdelta(remaining, ot_form.replace("\n", " "))), end="")
