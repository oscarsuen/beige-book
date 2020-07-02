import os
import pandas as pd

from tools import * # pylint: disable=wildcard-import, unused-wildcard-import

def filesizes():
    errorfile = open("out/csv/filesizes.csv", "w")
    errorfile.write("year,month,region,filesize\n")
    for year, month, region in gen(False):
        filename = get_txt_file((year, month, region))
        if os.path.exists(filename):
            errorfile.write(f"{year},{month:02d},{region},{os.path.getsize(filename)}\n")
    errorfile.close()

def missings():
    errorfile = open("out/csv/missing.csv", "w")
    errorfile.write("year,month,region\n")
    for year, month, region in gen(False):
        filename = get_txt_file((year, month, region))
        if not os.path.exists(filename):
            errorfile.write(f"{year},{month:02d},{region}\n")
    errorfile.close()

def analyze_missing(printing=True, writing=True):
    df = pd.read_csv("out/csv/missing.csv")
    empty = df.groupby(["year", "month"]).aggregate(count=('region', 'size')).query('count == 13')
    if printing:
        print(empty)
    if writing:
        empty.to_csv("out/csv/norelease.csv", columns=[])

    incomplete = df.groupby(['year', 'month']).filter(lambda x: len(x) != 13)
    if printing:
        print(incomplete)
    if writing:
        incomplete.to_csv("out/csv/incomplete.csv", index=False)

def analyze_filesize(printing=True, writing=True):
    df = pd.read_csv("out/csv/filesizes.csv")
    smallfiles = df.query('filesize < 1024')
    if printing:
        print(smallfiles)
    if writing:
        smallfiles.to_csv("out/csv/smallfiles.csv", columns=['year', 'month', 'region'], index=False)

if __name__ == "__main__":
    missings()
    filesizes()
    analyze_missing()
    analyze_filesize()
