# Beige Book
Scrape and analyze the Federal Reserve Beige Book reports

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
    - [ ] Check out `flair` package
- [x] Get exact dates of publication
- [x] Generate histograms
    - [x] Normalize values
    - [x] Check out outlier (`1971-01-bo` missing doc)
- [x] Regress national sentiment on regional sentiments
    - [ ] Do you add a constant here?
- [ ] Graph time series
    - [ ] Pretty up plots (title+legend)
    - [ ] Get GDP data
