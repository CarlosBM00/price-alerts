
from utils.file_dao import FileDAO
from utils.notifications import Notification

from scraper.platforms.amazon_scraper import AmazonScraper
from scraper.platforms.steam_scraper import SteamScraper

from models.product import Product

from typing import Optional, Tuple

from dotenv import load_dotenv
import os

load_dotenv()

CORREO_DEST = os.getenv("CORREO_DEST")


def process_result(comparison_result: Optional[Tuple[int, float, Product]]):
    
    if comparison_result is not None:
        
        old_price = comparison_result[1]
        producto = comparison_result[2]
        
        new_notification = Notification(CORREO_DEST)
        
        if comparison_result[0] == 1:
            print(f"El producto [{comparison_result[2].name}] ha SUBIDO de precio")
            # new_notification.send_email(new_notification.messages('subida').format(product_name, product_price, comparison_result[1]))
            
        elif comparison_result[0] == -1:
            print(f"El producto [{comparison_result[2].name}] ha BAJADO de precio")
            new_notification.send_email(new_notification.messages('bajada').format(producto.name, producto.price, old_price, producto.url))
            pass
        
        elif comparison_result[0] == 0:
            print(f"El producto [{comparison_result[2].name}] sigue con el mismo precio")
            pass

def scrape(url: str):
    if 'www.amazon.es' in url or 'amzn.eu' in url :
        scraped_product = AmazonScraper(url).scrape()
    elif 'store.steampowered.com' in url :
        scraped_product = SteamScraper(url).scrape()
    
    # print("\n", scraped_product, "\n")
    comparison_result = FileDAO().upsert_and_compare_prices(scraped_product)
    process_result(comparison_result)
    
def update_stored_records():
    stored_records = FileDAO().get_all_records()
    for record in stored_records.values:
        url = record[3]
        scrape(url)