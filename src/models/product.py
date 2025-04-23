from dataclasses import dataclass
from datetime import datetime

@dataclass
class Product:
    name: str
    price: float
    platform: str
    url: str
    last_update_date = str(datetime.now().strftime("%d/%m/%Y"))
