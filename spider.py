from bs4 import BeautifulSoup
import grequests

class Scraper:
    def __init__(self, url, include=None, exclude=None, output="scraped.txt"):
        self.url = url
        self.include = include if include else []
        self.exclude = exclude if exclude else []
        self.visited = set()
        self.output_file = output

    def should_process_link(self, link):
        if not isinstance(link, str) or not link.startswith('https://') or  link in self.visited:
            return False

        include_match = True
        if self.include:
            include_match = any(term in link for term in self.include)

        return include_match and not any(term in link for term in self.exclude)

    def process_urls(self, urls):
        if not urls:
            return
        requests = (grequests.get(u, timeout=10) for u in urls)
        new_links = []
        with open(self.output_file, 'a') as f:
            for i, response in grequests.imap_enumerated(requests, size=len(urls)):
                try:
                    if not response or response.status_code != 200:
                        print(f"Failed to fetch {urls[i]}")
                        continue
                    soup = BeautifulSoup(response.text, "html.parser")
                    source_url = urls[i]
                    for link in soup.find_all("a"):
                        href = link.get("href")
                        if self.should_process_link(href):
                            new_links.append(href)
                            self.visited.add(href)
                            result = f'["{source_url}", "{href}"]'
                            f.write(result + "\n")
                            print(result)
                except Exception as e:
                    print(f"Error processing {urls[i]}: {str(e)}")
                    continue
        self.process_urls(new_links)

    def start(self):
        with open(self.output_file, 'w') as f:
            pass
        self.process_urls([self.url])

scraper = Scraper(
    url="https://google.com",
    include=["google"],
    exclude=["youtube.com", "play"]
)
scraper.start()
