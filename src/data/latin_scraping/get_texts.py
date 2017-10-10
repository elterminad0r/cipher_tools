import sys
import time

from collections import Counter
from urllib.request import urlopen
from bs4 import BeautifulSoup

def show_author_links(auth, d=0):
    link = "http://www.thelatinlibrary.com/" + auth
    req = urlopen(link)
    soup = BeautifulSoup(req.read(), "html.parser")

    pages = []
    for page in soup.select("td a"):
        pages.append(page.get("href"))

    try:
        pref = Counter(i.split("/")[0] for i in pages).most_common(1)[0][0]

    except IndexError as e:
        if d < 3:
            sys.stderr.write("err on {}, waiting\n".format(auth))
            sys.stderr.flush()
            time.sleep(5)
            show_author_links(auth, d + 1)
        else:
            sys.stderr.write("done, printing auth\n")
            sys.stderr.flush()
            print(auth)
    else:
        print("\n".join(page for page in pages if page.startswith(pref)))
        sys.stderr.write("done {}\n".format(auth))
        sys.stderr.flush()

for line in sys.stdin:
    show_author_links(line.strip())
