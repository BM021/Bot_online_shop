import sqlite3
from datetime import datetime

connection = sqlite3.connect('dostavka.db')
sql = connection.cursor()


# Создаем таблицу #
# Таблица пользователей
sql.execute('CREATE TABLE IF NOT EXISTS users (telegram_id INTEGER, phone_number TEXT, name TEXT,'
            'loc_longitude REAL, loc_latitude REAL, reg_date DATETIME);')


# Таблица продуктов
sql.execute('CREATE TABLE IF NOT EXISTS products (product_id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'product_name TEXT, product_price REAL, product_description TEXT, product_photo TEXT,'
            'add_date DATETIME);')


# Корзина
sql.execute('CREATE TABLE IF NOT EXISTS user_cart (user_id INTEGER, product_name TEXT,'
            'product_count INTEGER, total_price REAL);')


# Таблица заказов
sql.execute('CREATE TABLE IF NOT EXISTS orders (user_id INTEGER, products TEXT, total_price REAL,'
            'order_date DATETIME);')


# Функционал #
# Проверка пользователя на наличия
def check_user(telegram_id):
    connection = sqlite3.connect('dostavka.db')
    sql = connection.cursor()

    checker = sql.execute('SELECT telegram_id FROM users WHERE telegram_id=?', (telegram_id,)).fetchone()

    if checker:
        return True

    else:
        return False


# Регистрация пользователя
def regist_user(telegram_id, phone_number, name, loc_longitude, loc_latitude):
    connection = sqlite3.connect('dostavka.db')
    sql = connection.cursor()

    sql.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?);',
                (telegram_id, phone_number, name, loc_longitude, loc_latitude, datetime.now()))

    connection.commit()


# Работа с продуктами
def create_product(product_name, product_price, product_description, product_photo):
    connection = sqlite3.connect('dostavka.db')
    sql = connection.cursor()

    sql.execute('INSERT INTO products (product_name, product_price, product_description, product_photo, add_date) '
                'VALUES (?, ?, ?, ?, ?);',
                (product_name, product_price, product_description, product_photo, datetime.now()))

    connection.commit()


# Получить все продукты
def get_all_products():
    connection = sqlite3.connect('dostavka.db')
    sql = connection.cursor()

    all_products = sql.execute('SELECT product_name FROM products;').fetchall()

    products = [i[0] for i in all_products]

    return products


# Получить конкретный продукт
def get_exact_product(product_name):
    connection = sqlite3.connect('dostavka.db')
    sql = connection.cursor()

    products_info = sql.execute('SELECT * FROM products WHERE product_name=?;', (product_name,)).fetchone()

    return products_info


# Админ панель #
# Удаление конкретного продукта из базы(админ панель) ДЗ
def delete_exact_product(product_name):
    connection = sqlite3.connect('dostavka.db')
    sql = connection.cursor()

    sql.execute('DELETE FROM products WHERE product_name=?;', (product_name,))

    connection.commit()


# Изменение цены конкретного продукта из базы(админ панель) ДЗ
def update_price_of_product(product_name, new_price):
    connection = sqlite3.connect('dostavka.db')
    sql = connection.cursor()

    sql.execute(f'UPDATE products SET product_price =? WHERE product_name =?;', (new_price, product_name))

    connection.commit()


# Фунукционал корзина #
# Добавление продуктов в корзину
def create_user_cart(user_id, product_name, product_count):
    connection = sqlite3.connect('dostavka.db')
    sql = connection.cursor()

    product_price = sql.execute('SELECT product_price FROM products WHERE product_name=?', (product_name,)).fetchone()
    total_price = product_price[0] * product_count

    sql.execute('INSERT INTO user_cart VALUES (?, ?, ?, ?);', (user_id, product_name, product_count, total_price))

    connection.commit()


# Вывод корзины определенного пользователя
def get_exact_user_cart(user_id):
    connection = sqlite3.connect('dostavka.db')
    sql = connection.cursor()

    user_cart = sql.execute('SELECT * FROM user_cart  WHERE user_id=?', (user_id,)).fetchall()

    return user_cart


# Удаление конкретного товара из корзины конкрентного пользователя
def delete_exact_product_from_user_cart(user_id, product_name):
    connection = sqlite3.connect('dostavka.db')
    sql = connection.cursor()

    sql.execute('DELETE FROM user_cart  WHERE user_id=? AND product_name=?', (user_id, product_name))

    connection.commit()


# Очистка корзины пользователя
def clear_user_cart(user_id):
    connection = sqlite3.connect('dostavka.db')
    sql = connection.cursor()

    sql.execute('DELETE FROM user_cart  WHERE user_id=?', (user_id,))

    connection.commit()