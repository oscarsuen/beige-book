# Beige Book
Scrape and analyze the Federal Reserve Beige Book reports

## TODO
- [x] Fix parsing errors
    - [x] Bug with `<br>` tag instead of `<br />` (no more breaks)
    - [x] Remove `<strong>` (ignored)
    - [ ] `&nbsp;` problem (check if this gets removed)
    - [ ] Delete "learn more" `<p>` at the bottom
- [x] Find missing/incomplete files
    - [x] Some files are empty
    - [x] Analyze `errors.txt`
- [x] Grab missing files
    - [ ] Grab missing `2016-0(4|6)-su` files
    - [ ] Grab missing `2015-07-*` files
    - [ ] Try to find missing `1971-01-bo`
