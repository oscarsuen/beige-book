import os
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
    errorfile = open("out/errors.csv", "w")
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
        except RuntimeError:
            errorfile.write(f"{year},{month:02d},{region}\n")
            print("n")
    errorfile.close()

def get_text(url):
    r = requests.get(url)
    if r.status_code == 404:
        raise RuntimeError
    assert r.status_code == 200
    txt = r.text.replace("<br>", "").replace("<br >", "")
    soup = BeautifulSoup(txt, features="html5lib")
    div = soup.find("div", class_="col-sm-12 col-lg-8 offset-lg-1")
    for e in div.find_all("br"):
        e.replace_with('\n')
    for e in div.find_all("strong"):
        e.extract()
    ps = div.find_all("p")[2:]
    raw_text = list(p.string for p in ps if p.string is not None)
    return [p.replace('\n', '').strip()+"\n" for p in raw_text]

def check_errors(threshold=1024):
    errorfile = open("out/smallfiles.csv", "w")
    errorfile.write("year,month,region\n")
    for year, month, region in gen():
        filename = f"txt/{year}/{month:02d}/{year}-{month:02d}-{region}.txt"
        if os.path.exists(filename) and os.path.getsize(filename) < threshold:
            errorfile.write(f"{year},{month:02d},{region}\n")
    errorfile.close()

if __name__ == "__main__":
    scrape()
    check_errors()
