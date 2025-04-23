import requests
from bs4 import BeautifulSoup
from models.product import Product

HEADERS = {'User-Agent': 
    'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/W.X.Y.Z Safari/537.36'}

class AmazonScraper:
    def __init__(self, url: str):
        self.url = url
        self.platform = "Amazon"

    def fetch_html(self):
        response = requests.get(self.url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text

    def parse_product(self, html: str) -> Product:
        soup = BeautifulSoup(html, 'html.parser')

        # Nombre del producto
        name_element = soup.find(attrs={'id': 'productTitle'})
        name = name_element.text.strip() if name_element else 'Name not found'

        # Precio
        price_element = soup.find('span', class_='a-price-whole')
        if price_element:
            price = price_element.text.strip().replace('.', '').replace(',', '')
            price = ''.join(filter(str.isdigit, price))  # clean up
        else:
            price = '0'

        return Product(
            platform=self.platform,
            name=name,
            price=float(price),
            url=self.url
        )

    def scrape(self) -> Product:
        html = self.fetch_html()
        return self.parse_product(html)
