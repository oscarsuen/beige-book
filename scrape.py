import os
import re
import csv
import requests
from bs4 import BeautifulSoup

def gen(skip=False):
    if skip:
        try:
            with open("out/norelease.csv", "r") as f:
                f.readline()
                norelease = {(int(y), int(m)) for y, m in csv.reader(f)}
            with open("out/incomplete.csv", "r") as f:
                f.readline()
                incomplete = {(int(y), int(m), r) for y, m, r in csv.reader(f)}
        except FileNotFoundError:
            skip = False
    regions = ("at", "bo", "ch", "cl", "da", "kc", "mi", "ny", "ph", "ri", "sf", "sl", "su")
    for year in range(1970, 2021):
        os.makedirs(f"txt/{year}", exist_ok=True)
        for month in range(1, 13):
            if skip and (year, month) in norelease:
                continue
            os.makedirs(f"txt/{year}/{month:02d}", exist_ok=True)
            for region in regions:
                if skip and (year, month, region) in incomplete:
                    continue
                yield year, month, region

def scrape(skip=False):
    errorfile = open("out/missing.csv", "w")
    errorfile.write("year,month,region\n")
    for year, month, region in gen(skip):
        print(f"{year}", f"{month:02d}", f"{region}", end=" ")
        header = "https://www.minneapolisfed.org/beige-book-reports/"
        url = header + f"{year}/{year}-{month:02d}-{region}"
        try:
            txt = get_text(url)
            with open(f"txt/{year}/{month:02d}/{year}-{month:02d}-{region}.txt", "w") as f:
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
    txt = r.text.replace("<br>", "").replace("<br >", "")
    soup = BeautifulSoup(txt, features="html5lib")
    div = soup.find("div", class_="col-sm-12 col-lg-8 offset-lg-1")
    # print(div.text)
    raw = re.sub(r"\s*\n\s*", "\n", div.text).strip()
    raw = raw.split("\n", 3)[3]
    raw = re.sub(r"\s*\n\s*", " ", raw)
    return raw

def filesizes():
    errorfile = open("out/filesizes.csv", "w")
    errorfile.write("year,month,region,filesize\n")
    for year, month, region in gen(False):
        filename = f"txt/{year}/{month:02d}/{year}-{month:02d}-{region}.txt"
        if os.path.exists(filename):
            errorfile.write(f"{year},{month:02d},{region},{os.path.getsize(filename)}\n")
    errorfile.close()

def missings():
    errorfile = open("out/missing.csv", "w")
    errorfile.write("year,month,region\n")
    for year, month, region in gen(False):
        filename = f"txt/{year}/{month:02d}/{year}-{month:02d}-{region}.txt"
        if not os.path.exists(filename):
            errorfile.write(f"{year},{month:02d},{region}\n")
    errorfile.close()

if __name__ == "__main__":
    scrape()
    missings()
    filesizes()
