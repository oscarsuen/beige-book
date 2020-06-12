import os
import re
import requests
from bs4 import BeautifulSoup

def gen():
    regions = ["at", "bo", "ch", "cl", "da", "kc", "mi", "ny", "ph", "ri", "sf", "sl", "su"]
    for year in range(1970, 2021):
        os.makedirs(f"txt/{year}", exist_ok=True)
        for month in range(1, 13):
            os.makedirs(f"txt/{year}/{month:02d}", exist_ok=True)
            for region in regions:
                yield year, month, region

def scrape():
    errorfile = open("out/missing.csv", "w")
    errorfile.write("year,month,region\n")
    for year, month, region in gen():
        print(f"{year}", f"{month:02d}", f"{region}", end=" ")
        header = "https://www.minneapolisfed.org/beige-book-reports/"
        url = header + f"{year}/{year}-{month:02d}-{region}"
        try:
            txt = get_text(url)
            with open(f"txt/{year}/{month:02d}/{year}-{month:02d}-{region}.txt", "w") as f:
                f.writelines(txt)
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
    lines = re.split(r"\n\s*\n", div.text)
    lines = [re.sub(r"\s*\n\s*", " ", p.strip())+"\n" for p in lines if not re.fullmatch(r"\s*", p)]
    return lines[3:]

def filesizes():
    errorfile = open("out/filesizes.csv", "w")
    errorfile.write("year,month,region,filesize\n")
    for year, month, region in gen():
        filename = f"txt/{year}/{month:02d}/{year}-{month:02d}-{region}.txt"
        if os.path.exists(filename):
            errorfile.write(f"{year},{month:02d},{region},{os.path.getsize(filename)}\n")
    errorfile.close()

def missings():
    errorfile = open("out/missings.csv", "w")
    errorfile.write("year,month,region\n")
    for year, month, region in gen():
        filename = f"txt/{year}/{month:02d}/{year}-{month:02d}-{region}.txt"
        if not os.path.exists(filename):
            errorfile.write(f"{year},{month:02d},{region}\n")
    errorfile.close()

if __name__ == "__main__":
    # scrape()
    good_url_1 = "https://www.minneapolisfed.org/beige-book-reports/1970/1970-05-at"
    good_url_2 = "https://www.minneapolisfed.org/beige-book-reports/1971/1971-05-sf"
    good_url_3 = "https://www.minneapolisfed.org/beige-book-reports/2001/2001-09-cl"
    bad_url_1 = "https://www.minneapolisfed.org/beige-book-reports/1971/1971-02-kc"
    bad_url_2 = "https://www.minneapolisfed.org/beige-book-reports/1971/1971-07-ch"
    lines = get_text(bad_url_2)
    print(lines)
