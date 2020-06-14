# Beige Book
Scrape and analyze the Federal Reserve Beige Book reports

## TODO
- [x] Bug with `<br>` tag instead of `<br />`
    - 1983 07 ri
    - Replacing all `br` tags removes subsequent paragraph
    - Fixed by ignoring line breaks
- [x] Remove `<strong>`
    - Ignored
- [ ] `&nbsp;` problem (check if this gets removed)
- [x] Some files are empty
    - Could be `<br>` problem
- [x] Analyze `errors.txt`
- [ ] Delete "learn more" `<p>` at the bottom
- [ ] Some are under `national-summary` instead of `su`
