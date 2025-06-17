"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from models import Product, Cart


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

    @pytest.fixture
    def product_1(self):
        return Product("book", 500, "This is a book", 100)
    @pytest.fixture
    def product_2(self):
        return Product("condenced_milk", 120, "This is a can of condenced_milk", 1000)


    @pytest.fixture
    def cart(self):
        return Cart()

    # Тесты метода Cart.add_product()
    def test_add_default_product_empty_cart(self, cart: Cart, product_1):
        cart.add_product(product_1)
        assert cart.products == {product_1: 1}

    def test_add_product_not_empty_cart(self, cart, product_1, product_2):
        cart.add_product(product_1, 1)
        cart.add_product(product_2, 2)
        assert cart.products == {product_1: 1, product_2: 2}

    def test_add_product_product_already_in_cart(self, cart, product_1):
        cart.add_product(product_1, 2)
        cart.add_product(product_1, 3)
        assert cart.products == {product_1: 5}

    def test_add_product_more_then_we_have(self, cart, product_1):
        with pytest.raises(ValueError):
            cart.add_product(product_1, product_1.quantity + 1)
        assert cart.products == {}

    #тесты метода Cart.remove_product()

    def test_remove_product_remove_small_amount(self, cart, product_1):
        cart.add_product(product_1, 10)
        cart.remove_product(product_1, 1)
        assert cart.products == {product_1: 9}

    def test_remove_product_remove_all(self, cart, product_1):
        cart.add_product(product_1, 10)
        cart.remove_product(product_1, 10)
        assert cart.products == {}

    def test_remove_product_remove_more(self, cart, product_1):
        cart.add_product(product_1, 10)
        cart.remove_product(product_1, 11)
        assert cart.products == {}

    def test_remove_product_default(self, cart, product_1):
        cart.add_product(product_1, 10)
        cart.remove_product(product_1)
        assert cart.products == {}

    def test_remove_product_not_in_the_cart(self, cart, product_1):
        with pytest.raises(ValueError):
            cart.remove_product(product_1)

    # тесты метода Cart.clear()
    def test_clear_not_empty_cart(self, cart, product_1):
        cart.add_product(product_1, 10)
        cart.clear()
        assert cart.products == {}

    def test_clear_empty_cart(self, cart):
        cart.clear()
        assert cart.products == {}

    # тесты метода Cart.get_total_price()

    def test_get_total_price_empty_cart(self, cart):
        assert cart.get_total_price() == 0.0

    def test_get_total_price_not_empty_cart(self, cart, product_1, product_2):
        cart.add_product(product_1, 5)
        cart.add_product(product_2, 3)
        assert cart.get_total_price() == product_1.price * 5 + product_2.price * 3

    # тесты метода Cart.buy()

    def test_buy_not_empty_cart(self, cart, product_1, product_2):
        product_1_initial_quantity = product_1.quantity
        product_2_initial_quantity = product_2.quantity
        cart.add_product(product_1, 5)
        cart.add_product(product_2, 3)
        cart.buy()
        assert product_1.quantity == product_1_initial_quantity - 5
        assert product_2.quantity == product_2_initial_quantity - 3
        assert cart.products == {}