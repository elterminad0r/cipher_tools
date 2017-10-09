from urllib.request import urlopen
from bs4 import BeautifulSoup

claud = urlopen("http://www.thelatinlibrary.com/claudian.html")

soup = BeautifulSoup(claud.read())

print("\n".join(i.get("href") for i in soup.select("a") if i.get("href").startswith("claudian/")))
