"""
Модуль содержит классы для клиентов, товаров и заказов.
Используется ООП: инкапсуляция, наследование, полиморфизм.
"""

import re
from datetime import datetime


class Person:
    """Базовый класс для персональных данных"""

    def __init__(self, name: str):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Имя должно быть непустой строкой.")
        self._name = value

    def __str__(self):
        return f"{self.__class__.__name__}(name={self._name})"


class Client(Person):
    """
    Класс клиента с контактными данными.

    Атрибуты
    --------
    name : str
        Имя клиента
    email : str
        Email клиента (проверяется через регулярное выражение)
    phone : str
        Номер телефона (формат +7XXXXXXXXXX)
    city : str
        Город проживания
    """

    def __init__(self, name: str, email: str, phone: str, city: str):
        super().__init__(name)
        self.email = email
        self.phone = phone
        self.city = city

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Некорректный email.")
        self._email = value

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        if not re.match(r"^\+7\d{10}$", value):
            raise ValueError("Телефон должен быть в формате +7XXXXXXXXXX.")
        self._phone = value

    def __str__(self):
        return f"Client(name={self.name}, email={self.email}, phone={self.phone}, city={self.city})"

    def __eq__(self, other):
        return isinstance(other, Client) and self.phone == other.phone


class Product:
    """
    Класс товара.

    Атрибуты
    --------
    name : str
        Название товара
    price : float
        Цена (должна быть положительной)
    category : str
        Категория товара
    """

    def __init__(self, name: str, price: float, category: str = "Общее"):
        self.name = name
        self.price = price
        self.category = category

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value <= 0:
            raise ValueError("Цена должна быть положительной.")
        self._price = value

    def __str__(self):
        return f"Product(name={self.name}, price={self.price}, category={self.category})"


class Order:
    """
    Класс заказа.

    Атрибуты
    --------
    client : Client
        Клиент, сделавший заказ
    products : list[Product]
        Список товаров
    order_date : str
        Дата заказа (в формате YYYY-MM-DD)
    status : str
        Статус заказа (по умолчанию "новый")
    """

    def __init__(self, client: Client, products: list, order_date: str = None, status: str = "новый"):
        self.client = client
        self.products = products
        self.order_date = order_date or datetime.now().strftime("%Y-%m-%d")
        self.status = status

    @property
    def total_cost(self) -> float:
        """Возвращает общую стоимость заказа."""
        return sum(p.price for p in self.products)

    def __str__(self):
        return f"Order(client={self.client.name}, total={self.total_cost}, date={self.order_date})"

    def __lt__(self, other):
        """Для сортировки по дате."""
        return self.order_date < other.order_date
