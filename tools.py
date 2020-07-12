import os
import csv

def gen(skip=False):
    if skip:
        try:
            with open("out/csv/norelease.csv", "r") as f:
                f.readline()
                norelease = {(int(y), int(m)) for y, m in csv.reader(f)}
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
                yield year, month, region

def get_txt_file(t):
    return f"txt/{t[0]}/{t[1]:02d}/{t[0]}-{t[1]:02d}-{t[2]}.txt"

def get_txt_string(year, month, region, printing=False):
    if printing: print(f"{year} {month:02d} {region}") # pylint: disable=multiple-statements
    filename = get_txt_file((year, month, region))
    with open(filename, "r") as f:
        s = f.read()
    return s
