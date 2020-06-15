import re
import cleantext

from tools import *

def clean():
    for t in gen(skip=True):
        filename = get_txt_file(t)
        with open(filename, "r") as f:
            old_txt = f.read()
        new_txt = old_txt
        new_txt = cleantext.clean(new_txt, fix_unicode=True, to_ascii=True, lower=False)
        new_txt = re.sub(r"[<>~*]", "", new_txt)
        # new_txt = new_txt.replace("&", " and ").replace("%", " percent")
        # new_txt = re.sub(r" -(?=[\d.])", " minus ", new_txt)
        # new_txt = new_txt.replace("+", " plus ").replace("=", " equals ")
        new_txt = re.sub(r"\s+", " ", new_txt)
        with open(filename, "w") as f:
            f.write(new_txt)

if __name__ == "__main__":
    clean()
