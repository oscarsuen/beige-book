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
- [ ] Run sentiment analysis
- [ ] Regress national sentiment on regional sentiments
- [ ] Graph time series
