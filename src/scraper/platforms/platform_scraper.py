import requests
from bs4 import BeautifulSoup
from models.product import Product

from abc import ABC, abstractmethod

HEADERS = {'User-Agent': 
    'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/W.X.Y.Z Safari/537.36'}

class AbstractScraper(ABC):
    def __init__(self, url: str, platform: str):
        self.url = url
        self.platform = platform

    def fetch_html(self):
        response = requests.get(self.url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text

    @abstractmethod
    def parse_product(self, html: str) -> Product:
        pass
    
    def scrape(self) -> Product:
        html = self.fetch_html()
        return self.parse_product(html)
