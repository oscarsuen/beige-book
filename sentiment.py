import nltk.sentiment
import textblob
import flair

from tools import * # pylint: disable=wildcard-import, unused-wildcard-import

def analyze_all():
    outfile = open("out/csv/sentiments.csv", "w")
    outfile.write("year,month,region,v_com,v_neg,v_neu,v_pos,t_sub,t_pol,f_score\n")
    vader = nltk.sentiment.vader.SentimentIntensityAnalyzer()
    tb = textblob.en.sentiments.PatternAnalyzer()
    fs = flair.models.TextClassifier.load('en-sentiment')
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
        f_score = fs.predict(flair.data.Sentence(s))
        print(f"score: {f_score[0].labels[0].score*(-1,1)[f_score[0].labels[0].value=='POSITIVE']}")
        outfile.write(f"{year},{month:02d},{region},{v_score['compound']},{v_score['neg']},{v_score['neu']},{v_score['pos']},{t_score.subjectivity},{t_score.polarity},{f_score[0].labels[0].score*(-1,1)[f_score[0].labels[0].value=='POSITIVE']}\n")
    outfile.close()

if __name__ == "__main__":
    analyze_all()
