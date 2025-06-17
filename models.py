class Product:
    """
    Класс продукта
    """
    name: str
    price: float
    description: str
    quantity: int

    def __init__(self, name, price, description, quantity):
        self.name = name
        self.price = price
        self.description = description
        self.quantity = quantity

    def check_quantity(self, quantity) -> bool:
        """
        Верните True если количество продукта больше или равно запрашиваемому
            и False в обратном случае
        """
        return True if self.quantity >= quantity else False

    def buy(self, quantity):
        """
        реализуйте метод покупки
            Проверьте количество продукта используя метод check_quantity
            Если продуктов не хватает, то выбросите исключение ValueError
        """
        # купить ноль или отрицательное количество книг тоже нельзя,
        # но в условиях проверки количества об этом ничего нет,
        # поэтому добавлю проверку в этот метод, ошибка будет та же
        if self.check_quantity(quantity) and quantity > 0:
            self.quantity -= quantity
        else:
            raise ValueError

    def __hash__(self):
        return hash(self.name + self.description)


class Cart:
    """
    Класс корзины. В нем хранятся продукты, которые пользователь хочет купить.
    TODO реализуйте все методы класса
    """

    # Словарь продуктов и их количество в корзине
    products: dict[Product, int]

    def __init__(self):
        # По-умолчанию корзина пустая
        self.products = {}

    def add_product(self, product: Product, buy_count: int = 1):
        """
        Метод добавления продукта в корзину.
        Если продукт уже есть в корзине, то увеличиваем количество
        """
        if product.check_quantity(buy_count):
            if product in self.products.keys():
                self.products[product] += buy_count
            else:
                self.products[product] = buy_count
        else:
            raise ValueError

    def remove_product(self, product: Product, remove_count=None):
        """
        Метод удаления продукта из корзины.
        Если remove_count не передан, то удаляется вся позиция
        Если remove_count больше, чем количество продуктов в позиции, то удаляется вся позиция
        """
        if product in self.products.keys():
            if remove_count is None or remove_count >= self.products[product]:
                del self.products[product]
            else:
                self.products[product] -= remove_count
        else:
            raise ValueError

    def clear(self):
        self.products = {}

    def get_total_price(self) -> float:
        total_price = 0.0
        for product, count in self.products.items():
            total_price += product.price * count
        return total_price

    def buy(self):
        """
        Метод покупки.
        Учтите, что товаров может не хватать на складе.
        В этом случае нужно выбросить исключение ValueError
        """
        for product, count in self.products.items():
            if product.check_quantity(count):
                product.buy(count)
            else:
                raise ValueError
        self.clear()
