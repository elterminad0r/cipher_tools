import sys

from urllib.request import urlopen
from bs4 import BeautifulSoup

def get_text(url):
    soup = BeautifulSoup(urlopen(url).read(), "html.parser")
    print(soup.get_text())
    sys.stderr.write("completed {}\n".format(url))
    sys.stderr.flush()

for url in sys.stdin:
    try:
        get_text("http://www.thelatinlibrary.com/{}".format(url))
    except Exception as e:
        sys.stderr.write("EXCEPTION OCCURRED: {}\n".format(e))
        sys.stderr.flush()
