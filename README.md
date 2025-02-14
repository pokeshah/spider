# Spider
Asynchronous web spider for simple, recursive crawling and link extraction with flexible filtering.

## Usage
See `spider.py` for OOP implementation. 

## Syntax
`
scraper = Scraper(
    url="https://google.com",
    include=["google"],
    exclude=["youtube.com", "play"]
)
scraper.start()
`

This will start a spider at url (google.com), and only continue searching if the url contains include (google) and doesn't include exclude (youtube.com or play)
