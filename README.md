# Beige Book
Scrape and analyze the Federal Reserve Beige Book reports.

We use several off-the-shelf text sentiment analysis tools to analyze the sentiment of the Fed's Beige Book reports from 1970--2020.

![GDP Growth Rate Comparison]
(out/figs/timeseries_suma_drgdp_int.png)

![Sentiment by District]
(out/figs/timeseries_district_vader.png)

## TODO
- [x] Fix parsing errors
    - [x] Bug with `<br>` tag instead of `<br />` (no more breaks)
    - [x] Remove `<strong>` (ignored)
    - [x] `&nbsp;` problem (check if this gets removed)
    - [ ] Delete "learn more" `<p>` at the bottom
- [x] Find missing/incomplete files
    - [x] Some files are empty
    - [x] Analyze `errors.txt`
- [x] Grab missing files
    - [x] Grab missing `2016-0(4|6)-su` files
    - [x] Grab missing `2015-07-*` files
    - [ ] Try to find missing `1971-01-bo`
- [x] Clean text
    - [ ] Replace `&%-+` with text?
- [x] Run sentiment analysis
    - [x] Check out `flair` package
    - [x] `flair` gives values `x<-0.5 | x>0.5` (fixed in analysis)
- [x] Get exact dates of publication
- [x] Generate histograms
    - [x] Normalize values
    - [x] Check out outlier (`1971-01-bo` missing doc)
- [x] Regress national sentiment on regional sentiments
    - [ ] Do you add a constant here?
    - [ ] See if coefficient sum to 1
- [x] Graph time series
    - [ ] Pretty up plots (title+legend)
    - [x] Get GDP data
    - [x] Check stock market data
    - [ ] Think about timing of Beige Book data
    - [ ] By region in a grid
- [ ] Investigate discrepancies between sentiment scores
    - [ ] In `su` `TextBlob` is high during 1974 recession and higher during 1990s boom
- [ ] Add info + pictures to `README.md`
