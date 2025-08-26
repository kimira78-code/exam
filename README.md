# Промышленная система учёта заказов

## Описание
Это прототип настольного приложения для менеджеров интернет-магазина, разработанный в качестве итоговой аттестации по курсу Python. 
Поддерживает: регистрацию, анализ, визуализацию, импорт/экспорт.

## Функции
- Добавление клиентов и заказов
- Проверка email и телефона (регулярные выражения)
- Хранение в SQLite
- Экспорт в CSV/JSON
- Визуализация: топ клиентов, динамика продаж, графы
- Хранение данных между запусками (файлы или SQLite).
- GUI на tkinter

## Описание модулей
- 'order_management_system/main.py': Главный файл для запуска приложения.
- 'order_management_system/models.py': Определяет классы данных: 'Client', 'Product', 'Order'.
- 'order_management_system/db.py': Отвечает за взаимодействие с базой данных SQLite.
- 'order_management_system/gui.py': Содержит код графического интерфейса.
- 'order_management_system/analysis': Реализует функции для анализа данных и их визуализации.
- 'order_management_system/test_models.py': unit-тест для модуля 'models'.

1. **Клонируйте репозиторий:**
    ```bash
    git clone < >
    cd Final
    ```

2. **Создайте и активируйте виртуальное окружение:**
    ```bash
    python -m venv venv
   # Для Windows
   venv\Scripts\activate
   # Для MacOS/Linux
   source venv/bin/activate
   ```
   
3. **Установите зависимости:**
    ```bash
   pip install -r requirements.txt
   ```
   
4. **Запустите приложение:**
   ```bash
   python -m project.main
    ```
   
## Запуск тестов

Для запуска unit-тестов выполните команду:

```bash
python -m inittest discover tests
```
