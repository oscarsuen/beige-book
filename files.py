import pandas as pd

def analyze_missingg():
    df = pd.read_csv("out/missings.csv")
    g = df.groupby(["year", "month"])
    c = g.aggregate(count=('region', 'size'))
    
