"""
solve challenge 10 lmao
"""

import argparse
import string

def format_tabula(subs):
    """
    Generate tabula recta from current substitutions
    """
    inverse_maps = [{b.upper(): a.upper()
                        for a, b in dct.items()} for dct in subs]
    return "\n".join("{}:{}{}"
                    .format(ltr, " ", " ".join(dct.get(ltr, " ")
                            for dct in inverse_maps))
                                    for ltr in string.ascii_uppercase)

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "file",  type=argparse.FileType("r"),
        help="ciphertext file")
    return parser.parse_args()

def display_text(txt, subs, pos):
    print(pos)
    out = []
    offset = 0
    for ind, c in enumerate(txt):
        if ind == pos:
            out.append("*")
            pos_offs = offset
        if c.isalpha():
            if c in subs[offset]:
                out.append(subs[offset][c])
            else:
                out.append(c)
            offset = (offset + 1) % 7
        else:
            out.append(c)
    print("".join(out))
    return pos_offs

def display_subs(subs):
    print(format_tabula(subs))
    for i in range(7):
        print("{}!m {}".format(i,
                " ".join("{}{}".format(a, b) for a, b in subs[i].items())))

def process_com(txt, pos_mut, subs, pos_offs):
    cmd = input("> ").strip()
    pos, = pos_mut
    if cmd == "h":
        while pos > 0:
            pos -= 1
            if txt[pos].isalpha():
                break
    elif cmd == "l":
        while pos < len(txt) - 1:
            pos += 1
            if txt[pos].isalpha():
                break
    elif cmd == "w":
        all_alpha = True
        while pos < len(txt) - 1:
            pos += 1
            if all_alpha:
                if not txt[pos].isalpha():
                    all_alpha = False
            else:
                if txt[pos].isalpha():
                    break
    elif cmd == "b":
        all_alpha = True
        while pos > 0:
            pos -= 1
            if all_alpha:
                if not txt[pos].isalpha():
                    all_alpha = False
            else:
                if txt[pos].isalpha():
                    break
    elif cmd == "#":
        while pos < len(txt) - 1:
            pos += 1
            if txt[pos].isalpha():
                pos_offs = (pos_offs + 1) % 7
            if txt[pos].isalpha() and txt[pos] not in subs[pos_offs]:
                break
    elif "!" in cmd:
        try:
            interval, rem = cmd.split("!")
            interval = int(interval)
            _, *rem = rem.split()
            for (a, b) in rem:
                assert a.isalpha()
                assert b.isalpha()
                subs[interval][a.upper()] = b.lower()
        except (ValueError, IndexError, AssertionError) as e:
            print(e)
    elif cmd.startswith("/"):
        try:
            _, lt = cmd
            subs[pos_offs][txt[pos]] = lt
        except (ValueError, IndexError, AssertionError) as e:
            print(e)
    pos_mut[0] = pos

def main(txt):
    pos = [0]
    subs = [{} for _ in range(7)]
    while True:
        display_subs(subs)
        offs = display_text(txt, subs, pos[0])
        process_com(txt, pos, subs, offs)

if __name__ == "__main__":
    args = get_args()
    main(args.file.read())
