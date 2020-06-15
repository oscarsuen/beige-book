import nltk.sentiment
import textblob

from tools import *

def analyze_all():
    outfile = open("out/sentiments.csv", "w")
    outfile.write("year,month,reggion,v_com,v_neg,v_neu,v_pos,t_sub,t_pol\n")
    vader = nltk.sentiment.vader.SentimentIntensityAnalyzer()
    tb = textblob.en.sentiments.PatternAnalyzer()
    for year, month, region in gen(skip=True):
        print(f"{year} {month:02d} {region}")
        filename = get_txt_file((year, month, region))
        with open(filename, "r") as f:
            s = f.read()
        v_score = vader.polarity_scores(s)
        for k in v_score:
            print(f"{k}: {v_score[k]}, ", end="")
        print()
        t_score = tb.analyze(s)
        print(f"subjectivity: {t_score.subjectivity}, polarity: {t_score.polarity}")
        outfile.write(f"{year},{month:02d},{region},{v_score['compound']},{v_score['neg']},{v_score['neu']},{v_score['pos']},{t_score.subjectivity},{t_score.polarity}\n")
    outfile.close()

if __name__ == "__main__":
    analyze_all()
