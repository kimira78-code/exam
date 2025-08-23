import unittest
from models import Client, Product, Order


class TestModels(unittest.TestCase):
    def test_client_valid(self):
        client = Client("Иван", "ivan@mail.ru", "+79991234567", "Москва")
        self.assertEqual(client.name, "Иван")

    def test_client_invalid_email(self):
        with self.assertRaises(ValueError):
            Client("Иван", "invalid", "+79991234567", "Москва")

    def test_product_price_positive(self):
        with self.assertRaises(ValueError):
            Product("Товар", -100)

    def test_order_total(self):
        p1 = Product("Книга", 300)
        p2 = Product("Ручка", 50)
        client = Client("Иван", "i@i.ru", "+79991234567", "СПб")
        order = Order(client, [p1, p2])
        self.assertEqual(order.total_cost, 350)


if __name__ == "__main__":
    unittest.main()
