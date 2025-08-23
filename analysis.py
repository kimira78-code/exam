"""
Функции анализа и визуализации данных: топ клиентов, динамика продаж, графы.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from models import Order
from typing import List


def top_clients_by_orders(orders: List[Order], n: int = 5):
    """Возвращает топ-n клиентов по количеству заказов."""
    df = pd.DataFrame([
        {"client": order.client.name, "date": order.order_date} for order in orders
    ])
    top = df["client"].value_counts().head(n)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top.values, y=top.index)
    plt.title(f"Топ-{n} клиентов по числу заказов")
    plt.xlabel("Количество заказов")
    plt.show()


def sales_trend(orders: List[Order]):
    """График динамики заказов по датам."""
    df = pd.DataFrame([{"date": order.order_date, "cost": order.total_cost} for order in orders])
    df["date"] = pd.to_datetime(df["date"])
    df = df.groupby("date")["cost"].sum().resample("D").sum().fillna(0)
    plt.figure(figsize=(12, 6))
    df.plot(title="Динамика продаж по дням")
    plt.ylabel("Сумма продаж")
    plt.grid()
    plt.show()


def client_product_graph(orders: List[Order]):
    """Построение графа связей клиентов через общие товары."""
    G = nx.Graph()
    for order in orders:
        client = order.client.name
        G.add_node(client)
        for product in order.products:
            product_name = product.name
            G.add_node(product_name)
            G.add_edge(client, product_name)
    plt.figure(figsize=(12, 8))
    nx.draw(G, with_labels=True, node_color="lightblue", font_size=10, node_size=800)
    plt.title("Граф связей клиентов и товаров")
    plt.show()
