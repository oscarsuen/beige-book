import os
import re
import requests
from bs4 import BeautifulSoup

from tools import *

def scrape(skip=False):
    errorfile = open("out/missing.csv", "w")
    errorfile.write("year,month,region\n")
    for year, month, region in gen(skip):
        print(f"{year}", f"{month:02d}", f"{region}", end=" ")
        header = "https://www.minneapolisfed.org/beige-book-reports/"
        url = header + f"{year}/{year}-{month:02d}-{region}"
        try:
            txt = get_text(url)
            with open(get_txt_file((year, month, region)), "w") as f:
                f.write(txt)
            print("y")
        except ValueError:
            errorfile.write(f"{year},{month:02d},{region}\n")
            print("n")
    errorfile.close()

def get_text(url):
    r = requests.get(url)
    if r.status_code == 404:
        raise ValueError
    if r.status_code != 200:
        raise RuntimeError(f"Status Code: {r.status_code}")
    soup = BeautifulSoup(r.text, features="html5lib")
    div = soup.find("div", class_="col-sm-12 col-lg-8 offset-lg-1")
    raw = re.sub(r"\s*\n\s*", "\n", div.text).strip()
    raw = raw.split("\n", 3)[3]
    return raw

if __name__ == "__main__":
    scrape()
    # with open("txt/2016/04/2016-04-su.txt", "w") as f:
        # f.write(get_text("https://www.minneapolisfed.org/beige-book-reports/2016/2016-04-national-summary"))
    # with open("txt/2016/06/2016-06-su.txt", "w") as f:
        # f.write(get_text("https://www.minneapolisfed.org/beige-book-reports/2016/2016-06-national-summary"))
