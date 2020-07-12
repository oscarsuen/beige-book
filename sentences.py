import nltk
import nltk.data
from tools import * # pylint: disable=wildcard-import, unused-wildcard-import

def split_sentences(printing=False):
    m = nltk.data.load('tokenizers/punkt/english.pickle')
    for year, month, region in gen(skip=True):
        if printing: print(f"{year} {month:02d} {region}") # pylint: disable=multiple-statements
        s = get_txt_string(year, month, region)
        l = m.tokenize(s)
        fn = f"txt-split/{year}/{month:02d}/{year}-{month:02d}-{region}.txt"
        with open(fn, "w") as f:
            f.write("\n".join(l))

if __name__ == "__main__":
    split_sentences(printing=True)
