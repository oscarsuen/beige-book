import pandas as pd

def analyze_missing(printing=True, writing=True):
    df = pd.read_csv("out/missing.csv")
    empty = df.groupby(["year", "month"]).aggregate(count=('region', 'size')).query('count == 13')
    if printing:
        print(empty)
    if writing:
        empty.to_csv("out/norelease.csv", columns=[])

    incomplete = df.groupby(['year', 'month']).filter(lambda x: len(x) != 13)
    if printing:
        print(incomplete)
    if writing:
        incomplete.to_csv("out/incomplete.csv", index=False)

def analyze_filesize(printing=True, writing=True):
    df = pd.read_csv("out/filesizes.csv")
    smallfiles = df.query('filesize < 1024')
    if printing:
        print(smallfiles)
    if writing:
        smallfiles.to_csv("out/smallfiles.csv", columns=['year', 'month', 'region'], index=False)

if __name__ == "__main__":
    analyze_missing()
    analyze_filesize()
