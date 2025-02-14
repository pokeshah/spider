from bs4 import BeautifulSoup
import grequests


class Scrape:
    def __init__(self, url, include="", exclude="", o="scraped.txt"):
        self.url = url
        self.include = include
        self.exclude = exclude
        self.visited = []
        self.f = open(o, "w")

    def requestandprocess(self, urls):
        rs = (grequests.get(u) for u in urls)
        for request in grequests.imap_enumerated(rs, size=len(urls)):
            soup = BeautifulSoup(request[1].text, "html.parser")
            links = []
            for link in soup.find_all("a"):
                link = link.get("href")
                if type(link) is str:
                    if link.startswith('https://') and link not in self.visited and self.include in link and self.exclude not in link:
                        links.append(link)
                        self.visited.append(link)
                        parced = f'["{urls[request[0]]}", "{link}"]'
                        self.f.write(parced + "\n")
                        print(parced)
            self.requestandprocess(links)

    def start(self):
        self.requestandprocess([self.url])

Scraper = Scrape("https://google.com", exclude="play")
Scraper.start()
