"""
Графический интерфейс для управления клиентами, заказами и анализом.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from models import Client, Product, Order
from db import Database
from analysis import top_clients_by_orders, sales_trend, client_product_graph


class OrderApp:
    def __init__(self, root: tk.Tk):
        self.db = Database()
        self.root = root
        self.root.title("Система учёта заказов")
        self.root.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        # Создание вкладок
        tab_control = ttk.Notebook(self.root)
        tab_control.pack(expand=1, fill="both")

        # Вкладка: Клиенты
        tab_clients = ttk.Frame(tab_control)
        tab_control.add(tab_clients, text="Клиенты")

        tk.Label(tab_clients, text="Имя:").grid(row=0, column=0)
        self.name_entry = tk.Entry(tab_clients)
        self.name_entry.grid(row=0, column=1)

        tk.Label(tab_clients, text="Email:").grid(row=1, column=0)
        self.email_entry = tk.Entry(tab_clients)
        self.email_entry.grid(row=1, column=1)

        tk.Label(tab_clients, text="Телефон (+7...):").grid(row=2, column=0)
        self.phone_entry = tk.Entry(tab_clients)
        self.phone_entry.grid(row=2, column=1)

        tk.Label(tab_clients, text="Город:").grid(row=3, column=0)
        self.city_entry = tk.Entry(tab_clients)
        self.city_entry.grid(row=3, column=1)

        tk.Button(tab_clients, text="Добавить клиента", command=self.add_client).grid(row=4, column=0, columnspan=2)

        # Вкладка: Заказы
        tab_orders = ttk.Frame(tab_control)
        tab_control.add(tab_orders, text="Заказы")

        tk.Label(tab_orders, text="Телефон клиента:").grid(row=0, column=0)
        self.order_phone = tk.Entry(tab_orders)
        self.order_phone.grid(row=0, column=1)

        tk.Label(tab_orders, text="Товар (название, цена):").grid(row=1, column=0)
        self.product_name = tk.Entry(tab_orders)
        self.product_price = tk.Entry(tab_orders)
        self.product_name.grid(row=1, column=1)
        self.product_price.grid(row=1, column=2)

        tk.Button(tab_orders, text="Добавить заказ", command=self.add_order).grid(row=2, column=0, columnspan=3)

        # Вкладка: Анализ
        tab_analysis = ttk.Frame(tab_control)
        tab_control.add(tab_analysis, text="Анализ")

        tk.Button(tab_analysis, text="Топ 5 клиентов", command=lambda: top_clients_by_orders(self.db.get_orders())).pack(pady=10)
        tk.Button(tab_analysis, text="Динамика продаж", command=lambda: sales_trend(self.db.get_orders())).pack(pady=10)
        tk.Button(tab_analysis, text="Граф клиентов-товаров", command=lambda: client_product_graph(self.db.get_orders())).pack(pady=10)

        # Экспорт/Импорт
        tab_io = ttk.Frame(tab_control)
        tab_control.add(tab_io, text="Импорт/Экспорт")

        tk.Button(tab_io, text="Экспорт в CSV", command=self.export_csv).pack(pady=5)
        tk.Button(tab_io, text="Импорт из CSV", command=self.import_csv).pack(pady=5)
        tk.Button(tab_io, text="Экспорт в JSON", command=self.export_json).pack(pady=5)

    def add_client(self):
        try:
            client = Client(
                self.name_entry.get(),
                self.email_entry.get(),
                self.phone_entry.get(),
                self.city_entry.get()
            )
            self.db.add_client(client)
            messagebox.showinfo("Успех", "Клиент добавлен!")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def add_order(self):
        try:
            phone = self.order_phone.get()
            name = self.product_name.get()
            price = float(self.product_price.get())
            product = Product(name, price)
            client = Client("Temp", "temp@temp.ru", phone, "Город")
            order = Order(client, [product])
            self.db.add_order(order)
            messagebox.showinfo("Успех", "Заказ добавлен!")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def export_csv(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv")
        if filename:
            self.db.export_to_csv(filename)
            messagebox.showinfo("Экспорт", "Данные экспортированы в CSV")

    def import_csv(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filename:
            self.db.import_from_csv(filename)
            messagebox.showinfo("Импорт", "Данные импортированы из CSV")

    def export_json(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json")
        if filename:
            self.db.export_to_json(filename)
            messagebox.showinfo("Экспорт", "Данные экспортированы в JSON")

    def close(self):
        self.db.close()


# Запуск GUI
def run_gui():
    root = tk.Tk()
    app = OrderApp(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (app.close(), root.destroy()))
    root.mainloop()
