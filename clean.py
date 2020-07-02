import re
import cleantext

from tools import *

def clean():
    for t in gen(skip=True):
        filename = get_txt_file(t)
        with open(filename, "r") as f:
            old_txt = f.read()
        new_txt = old_txt
        new_txt = cleantext.clean(new_txt, fix_unicode=True, to_ascii=True, lower=False, no_urls=True)

        new_txt = re.sub(r"For more information about District economic conditions,? visit: URL", "", new_txt)
        new_txt = new_txt.replace("%-", " percent to ").replace("%", " percent")
        new_txt = new_txt.replace(" & ", " and ")
        # new_txt = new_txt.replace("&", " and ") # ex. R&D
        # new_txt = re.sub(r" -(?=[\d.])", " minus ", new_txt)
        # new_txt = new_txt.replace("+", " plus ")
        new_txt = new_txt.replace("=", " equals ") # only one instance

        new_txt = re.sub(r"[<>~*]", "", new_txt)
        new_txt = re.sub(r"\-\-+", " , ", new_txt)
        new_txt = re.sub(r"\?(?=[\w])", "? ", new_txt).replace(" ?", "?")
        new_txt = re.sub(r"\s+,", ",", new_txt).replace(",,", ",")
        new_txt = re.sub(r"\s+\.(?=[^0-9])", " ", new_txt)
        new_txt = new_txt.replace("...", " ")
        new_txt = new_txt.replace("..", ".").replace(",.", ",") # ".," is legitimate
        new_txt = new_txt.replace("[", "").replace("]", "") # parentheses are legitimate

        new_txt = re.sub(r"\s+", " ", new_txt)
        new_txt = new_txt.strip()
        with open(filename, "w") as f:
            f.write(new_txt)

if __name__ == "__main__":
    clean()
