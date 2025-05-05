import tempfile
import os
import pandas as pd
from datetime import datetime

from utils.file_dao import FileDAO
from models.product import Product

def create_dummy_product(url="https://example.com"):
    return Product(
        platform="Amazon",
        name="Producto Test",
        price=25,
        url=url
    )

def test_create_file_and_insert():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
        dao = FileDAO(file_path=temp_file.name)

        assert os.path.isfile(temp_file.name)
        assert list(dao.records.columns) == ['Plataforma', 'Nombre', 'Precio_euros', 'URL', 'Fecha_última_búsqueda']

        product = create_dummy_product("https://store.steampowered.com/app/2169200/Sniper_Elite_Resistance/")
        dao.upsert_record(product)

        df = pd.read_csv(temp_file.name)
        assert len(df) == 1
        assert df["Nombre"].iloc[0] == "Producto Test"

    os.remove(temp_file.name)

def test_price_comparison():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
        dao = FileDAO(file_path=temp_file.name)

        # Inserta producto con precio 25
        product = create_dummy_product()
        dao.upsert_record(product)

        # Actualiza con precio 20
        product.price = 20
        result = dao.upsert_and_compare_prices(product)
        assert result[0] == -1  # Ha bajado

        # Actualiza con precio 20
        result = dao.upsert_and_compare_prices(product)
        assert result[0] == 0  # Igual

        # Actualiza con precio 30
        product.price = 30
        result = dao.upsert_and_compare_prices(product)
        assert result[0] == 1  # Ha subido

    os.remove(temp_file.name)
