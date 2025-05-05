import pytest
from unittest.mock import patch, MagicMock
from scraper.main_scraper import process_result
from models.product import Product

@pytest.fixture
def dummy_product():
    return Product(name="Test Product", price=9.99, platform="test", url="http://example.com/product")

@patch("scraper.main_scraper.Notification")
def test_process_result_price_increase(mock_notification_class, dummy_product):
    mock_notification = MagicMock()
    mock_notification_class.return_value = mock_notification

    comparison_result = (1, 8.99, dummy_product)  # Subida de precio

    process_result(comparison_result)

    mock_notification.send_email.assert_not_called()  # No se manda email en caso de subida

@patch("scraper.main_scraper.Notification")
def test_process_result_price_decrease(mock_notification_class, dummy_product):
    mock_notification = MagicMock()
    mock_notification.messages.return_value = "El producto {0} ha bajado a {1} desde {2} - {3}"
    mock_notification_class.return_value = mock_notification

    comparison_result = (-1, 15.99, dummy_product)  # Bajada de precio

    process_result(comparison_result)

    mock_notification.send_email.assert_called_once_with(
        "El producto Test Product ha bajado a 9.99 desde 15.99 - http://example.com/product"
    )

@patch("scraper.main_scraper.Notification")
def test_process_result_price_same(mock_notification_class, dummy_product):
    mock_notification = MagicMock()
    mock_notification_class.return_value = mock_notification

    comparison_result = (0, 9.99, dummy_product)  # Mismo precio

    process_result(comparison_result)

    mock_notification.send_email.assert_not_called()

def test_process_result_none():
    # No se debe hacer nada si el resultado es None
    assert process_result(None) is None
