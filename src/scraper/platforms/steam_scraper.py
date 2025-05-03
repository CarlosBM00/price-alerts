import requests
from bs4 import BeautifulSoup
from models.product import Product

from .platform_scraper import AbstractScraper

class SteamScraper(AbstractScraper):

    def __init__(self, url: str):
        super().__init__(url, "Steam")

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