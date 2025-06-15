"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from models import Product


@pytest.fixture
def product() -> Product:
    return Product("book", 100, "This is a book", 1000)


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity_less(self, product):
        #проверки на метод check_quantity
        assert product.check_quantity(product.quantity - 1)
    def test_product_check_quantity_equal(self, product):
        assert product.check_quantity(product.quantity)
    def test_product_check_quantity_more(self, product):
        assert not product.check_quantity(product.quantity + 1)

    def test_product_buy(self, product):
        #проверки на метод buy
        initial_quantity = product.quantity
        buy_quantity = 5
        product.buy(buy_quantity)
        assert product.quantity == initial_quantity - buy_quantity


    def test_product_buy_more_than_available(self, product):
        initial_quantity = product.quantity
        buy_quantity = product.quantity + 1
        with pytest.raises(ValueError):
            product.buy(buy_quantity)
        assert product.quantity == initial_quantity
    def test_product_buy_not_positive(self, product):
        initial_quantity = product.quantity
        buy_quantity = 0
        with pytest.raises(ValueError):
            product.buy(buy_quantity)
        assert product.quantity == initial_quantity

    def test_product_buy_all(self, product):
        product.buy(product.quantity)
        assert product.quantity == 0


class TestCart:
    """
    Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """
