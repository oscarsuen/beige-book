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

def get_date(url):
    r = requests.get(url)
    if r.status_code == 404:
        raise ValueError
    if r.status_code != 200:
        raise RuntimeError(f"Status Code: {r.status_code}")
    soup = BeautifulSoup(r.text, features="html5lib")
    div = soup.find("div", class_="col-sm-12 col-lg-8 offset-lg-1")
    raw = re.sub(r"\s*\n\s*", "\n", div.text).strip()
    raw = raw.split("\n", 3)[2]
    return raw

def scrape_dates():
    outfile = open("out/dates.csv", "w")
    outfile.write("year,month,day\n")
    for year, month, region in gen(skip=True):
        if region == 'at':
            print(f"{year} {month}")
            header = "https://www.minneapolisfed.org/beige-book-reports/"
            url = header + f"{year}/{year}-{month:02d}-{region}"
            txt = get_date(url)
            day = int(txt.split()[1][:-1])
            outfile.write(f"{year},{month},{day}\n")
    outfile.close()

def get_econ_data():
    r = requests.get("https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=GDPC1&scale=left&cosd=1947-01-01&coed=2020-01-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Quarterly&fam=avg&fgst=lin&fgsnd=2009-06-01&line_index=1&transformation=pch&vintage_date=2020-06-15&revision_date=2020-06-15&nd=1947-01-01")
    with open("out/gdp.csv", "w") as f:
        f.write(r.text)
    r = requests.get("https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=UNRATE&scale=left&cosd=1948-01-01&coed=2020-05-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2009-06-01&line_index=1&transformation=lin&vintage_date=2020-06-19&revision_date=2020-06-19&nd=1948-01-01")
    with open("out/unrate.csv", "w") as f:
        f.write(r.text)
    r = requests.get("https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=WILL5000INDFC&scale=left&cosd=1970-12-31&coed=2020-06-18&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=pc1&vintage_date=2020-06-19&revision_date=2020-06-19&nd=1970-12-31")
    with open("out/stocks.csv", "w") as f:
        f.write(r.text)
    with open("out/recessions.csv", "w") as f:
        f.write("""
start,end
1969-12,1970-11
1973-11,1975-03
1980-01,1980-07
1981-07,1982-11
1990-07,1991-03
2001-03,2001-11
2007-12,2009-06
2020-02,2020-06""")

if __name__ == "__main__":
    # scrape()
    # scrape_dates()
    get_econ_data()
    # with open("txt/2016/04/2016-04-su.txt", "w") as f:
        # f.write(get_text("https://www.minneapolisfed.org/beige-book-reports/2016/2016-04-national-summary"))
    # with open("txt/2016/06/2016-06-su.txt", "w") as f:
        # f.write(get_text("https://www.minneapolisfed.org/beige-book-reports/2016/2016-06-national-summary"))
