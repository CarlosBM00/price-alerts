import requests
from bs4 import BeautifulSoup
from models.product import Product

from .platform_scraper import AbstractScraper

class AmazonScraper(AbstractScraper):
    def __init__(self, url: str):
        super().__init__(url, "Amazon")

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