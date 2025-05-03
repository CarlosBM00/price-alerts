import os
import csv
import pandas as pd
from models.product import Product

pd.set_option('display.max_columns', None)

class FileDAO:
    def __init__(self, file_path="price-alerts/data/products.csv"):
        self.file_name = file_path
        self.create_file_if_not_exists()
        self.records = pd.read_csv(self.file_name, sep=',')

    def create_file_if_not_exists(self):
        if not os.path.isfile(self.file_name) or os.path.getsize(self.file_name) == 0:
            with open(self.file_name, 'a', encoding='UTF8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Plataforma', 'Nombre', 'Precio_euros', 'URL', 'Fecha_última_búsqueda'])

    def get_all_records(self):
        """Devuelve todos los registros almacenados en el archivo CSV."""
        
        return self.records

    def get_single_record(self, url):
        """Devuelve un único registro coincidente con la URL proporcionada."""
        
        return self.records.loc[self.records["URL"] == url]

    def upsert_record(self, scraped_product: Product):
        """
        Inserta o actualiza un producto.
        Columnas esperadas: [Plataforma, Nombre, Precio, URL, Fecha última búsqueda]
        """
        
        new_record_df = pd.DataFrame([[scraped_product.platform, 
                                      scraped_product.name, 
                                      scraped_product.price, 
                                      scraped_product.url, 
                                      scraped_product.last_update_date]], columns=self.records.columns)

        if scraped_product.url not in self.records['URL'].values:
            self.records = pd.concat([self.records, new_record_df], ignore_index=True)
        else:
            idx = self.records["URL"] == scraped_product.url
            self.records.loc[idx, ["Plataforma", "Nombre", "Precio_euros", "Fecha_última_búsqueda"]] = [
                scraped_product.platform, scraped_product.name, scraped_product.price, scraped_product.last_update_date
            ]

        self.records.to_csv(self.file_name, index=False)

    def delete_record(self, index):
        """Elimina un registro por índice."""
        self.records = self.records.drop(index)
        self.records.to_csv(self.file_name, index=False)

    def upsert_and_compare_prices(self, scraped_product: Product):
        """
        Inserta o actualiza un producto y compara su precio actual con el almacenado previamente.
        Devuelve:
            (-1, precio_anterior) si el precio ha bajado
            ( 0, precio_anterior) si el precio no ha cambiado
            ( 1, precio_anterior) si el precio ha subido
            None si no hay precio anterior
        """
        try:
            current_price = int(scraped_product.price)
        except ValueError:
            print(f"[ERROR] Precio no válido para {scraped_product.name}: {scraped_product.price}")
            return None

        existing = self.records[self.records["URL"] == scraped_product.url]

        self.upsert_record(scraped_product)
        
        if existing.empty:
            return None

        stored_price = int(existing["Precio_euros"].iloc[0])

        if stored_price > current_price:
            return -1, stored_price, scraped_product
        elif stored_price == current_price:
            return 0, stored_price, scraped_product
        else:
            return 1, stored_price, scraped_product
