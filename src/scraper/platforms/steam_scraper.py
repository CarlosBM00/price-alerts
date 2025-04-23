import requests
from bs4 import BeautifulSoup
from models.product import Product

HEADERS = {'User-Agent': 
    'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/W.X.Y.Z Safari/537.36'}

class SteamScraper:

    def __init__(self, url: str):
        self.url = url
        self.platform = "Steam"

    def fetch_html(self):
        response = requests.get(self.url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text

    def parse_product(self, html: str) -> Product:
        soup = BeautifulSoup(html, 'html.parser')

        name_element = soup.find(attrs={'id':'appHubAppName'})
        name = name_element.text.strip() if name_element else 'Name not found'
        
        price_element = soup.find('div', class_='discount_final_price')
        if not price_element:
            price_element = soup.find('div', class_='game_purchase_price price')
        
        price = price_element.text.split(',')[0].strip() if price_element else 'Price not found'

        return Product(
            platform=self.platform,
            name=name,
            price=float(price),
            url=self.url
        )

    def scrape(self) -> Product:
        html = self.fetch_html()
        return self.parse_product(html)
