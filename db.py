"""
Модуль для работы с базой данных SQLite.
Создание таблиц, CRUD-операции, импорт/экспорт в CSV/JSON.
"""

import sqlite3
import json
import csv
from typing import List
from models import Client, Product, Order

DB_FILE = "shop.db"

class Database:
    def __init__(self, db_name="orders.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    phone TEXT NOT NULL UNIQUE,
                    city TEXT
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    price REAL NOT NULL,
                    category TEXT
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    client_id INTEGER,
                    product_ids TEXT,
                    order_date TEXT,
                    status TEXT,
                    FOREIGN KEY (client_id) REFERENCES clients (id)
                )
            """)

    def add_client(self, client: Client):
        try:
            self.conn.execute(
                "INSERT INTO clients (name, email, phone, city) VALUES (?, ?, ?, ?)",
                (client.name, client.email, client.phone, client.city)
            )
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Ошибка добавления клиента: {e}")

    def get_clients(self) -> List[Client]:
        cur = self.conn.cursor()
        cur.execute("SELECT name, email, phone, city FROM clients")
        return [Client(*row) for row in cur.fetchall()]

    def add_product(self, product: Product):
        self.conn.execute(
            "INSERT INTO products (name, price, category) VALUES (?, ?, ?)",
            (product.name, product.price, product.category)
        )
        self.conn.commit()

    def get_products(self) -> List[Product]:
        cur = self.conn.cursor()
        cur.execute("SELECT name, price, category FROM products")
        return [Product(*row) for row in cur.fetchall()]

    def add_order(self, order: Order):
        client_id = self._get_client_id(order.client.phone)
        product_ids = ",".join(str(self._get_or_create_product(p)) for p in order.products)
        self.conn.execute(
            "INSERT INTO orders (client_id, product_ids, order_date, status) VALUES (?, ?, ?, ?)",
            (client_id, product_ids, order.order_date, order.status)
        )
        self.conn.commit()

    def get_orders(self) -> List[Order]:
        cur = self.conn.cursor()
        cur.execute("""
            SELECT c.name, c.email, c.phone, c.city, o.product_ids, o.order_date, o.status
            FROM orders o
            JOIN clients c ON o.client_id = c.id
        """)
        orders = []
        products = {p.name: p for p in self.get_products()}
        for row in cur.fetchall():
            client_data = row[:4]
            client = Client(*client_data)
            product_names = [pid.split(":")[0] for pid in row[4].split(",")]
            prod_list = [products[name] for name in product_names if name in products]
            order = Order(client, prod_list, row[5], row[6])
            orders.append(order)
        return orders

    def _get_client_id(self, phone: str) -> int:
        cur = self.conn.cursor()
        cur.execute("SELECT id FROM clients WHERE phone = ?", (phone,))
        result = cur.fetchone()
        if not result:
            raise ValueError("Клиент не найден.")
        return result[0]

    def _get_or_create_product(self, product: Product) -> int:
        cur = self.conn.cursor()
        cur.execute("SELECT id FROM products WHERE name = ?", (product.name,))
        result = cur.fetchone()
        if result:
            return result[0]
        self.add_product(product)
        return self.conn.lastrowid

    def export_to_csv(self, filename="clients.csv"):
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Имя", "Email", "Телефон", "Город"])
            for client in self.get_clients():
                writer.writerow([client.name, client.email, client.phone, client.city])

    def import_from_csv(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                client = Client(row["Имя"], row["Email"], row["Телефон"], row["Город"])
                self.add_client(client)

    def export_to_json(self, filename="orders.json"):
        orders = []
        for order in self.get_orders():
            orders.append({
                "client": order.client.__dict__,
                "products": [p.__dict__ for p in order.products],
                "order_date": order.order_date,
                "status": order.status,
                "total": order.total_cost
            })
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(orders, f, ensure_ascii=False, indent=2)

    def close(self):
        self.conn.close()
