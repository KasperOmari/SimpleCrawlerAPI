import requests, re
from urllib.parse import urljoin, urlparse
import collections
from lxml import html

class Crawler:
    def __init__(self):
        self.linksFound = dict()
        self.goodLinks = set()
        self.badLinks = set()
        self.queue = collections.deque()

    def crawl(self, baseUrl, depth):
        try:
            self.validateDepth(depth)
        except ValueError as e:
            return e.args[0]

        print ("Crawler is running for: {}, with depth: {}".format(baseUrl, depth))
        try:
            self.BFS(baseUrl, depth)
        except Exception as e:
            return e.args[0]

        print("Crawler finished successfully")
        return self.linksFound


    def validateDepth(self, depth):
        self.validateInteger(depth)
        self.isNonNigative(depth)


    def validateInteger(self, depth):
        try:
            int(depth)
        except ValueError:
            raise ValueError("{'Error': 'Depth Must be an integer'}")


    def isNonNigative(self, depth):
        if int(depth) < 0:
            raise ValueError("{'Error': 'Depth Must be positive'}")
        
    def BFS(self, baseUrl, depth):
        depth = int(depth)
        self.queue.append((baseUrl, 0))  
        self.goodLinks.add(baseUrl)

        while len(self.queue):
            url, level = self.queue.popleft()

            if len(url) < 1:
                self.badLinks.add(url)
                break

            if level == depth:
                self.queue.clear()
                break
            
            response = requests.get(url)
            if (response.status_code == 400 or response.status_code == 403 or response.status_code == 404) : 
                print("Bad Request")
                break 

            parsed_body = html.fromstring(response.content)

            links = {urljoin(response.url, url) for url in parsed_body.xpath('//a/@href') if urljoin(response.url, url).startswith(baseUrl)}

            length = len(links)

            for link in (links - self.goodLinks):
                self.goodLinks.add(link)
                self.queue.append((link, level+1))

        self.linksFound.update({"available": list(self.goodLinks)})
        self.linksFound.update({"not-available": list(self.badLinks)})
