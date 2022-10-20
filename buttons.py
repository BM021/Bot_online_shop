from telebot import types
import database_dostavka


# Конпки осного меню
def main_menu_buttons():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Каталог')
    button2 = types.KeyboardButton('Связаться с нами')

    kb.add(button1, button2)

    return kb


# Меню продуктов
def products_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    cart_button = types.KeyboardButton('Корзина')
    main_menu = types.KeyboardButton('Основное меню')
    kb.row(main_menu, cart_button)

    products = database_dostavka.get_all_products()

    for product in products:
        kb.add(product)

    return kb


# Выбор количиство продуктов
def product_count_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for count in range(1, 11):
        kb.add(str(count))

    return kb


# Кнопки корзины
def basket_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    order = types.KeyboardButton('Оформить заказ')
    delete_cart = types.KeyboardButton('Очистить корзину')
    back = types.KeyboardButton('Основное меню')

    kb.add(order, delete_cart, back)

    return kb


# Оформление заказа
def confirm_order_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    confirm = types.KeyboardButton('Потвердить')
    cancel = types.KeyboardButton('Отменить')

    kb.row(cancel, confirm)

    return kb


# Локация
def location_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    location = types.KeyboardButton('Отправить локацию', request_location=True)

    kb.add(location)

    return kb


# Контакт
def phone_number_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    phone_number = types.KeyboardButton('Отправить контакт', request_contact=True)

    kb.add(phone_number)

    return kb


# Админка кнопка добавление продукта
def admin_product_buttons():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    add_product = types.KeyboardButton('Добавить продукт')
    delete_product = types.KeyboardButton('Удалить продукт')
    update_product_price = types.KeyboardButton('Изменить цену продукта')

    kb.add(add_product, delete_product)
    kb.row(update_product_price)

    return kb


# Админка кнопка удаление продукта
def admin_all_product_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    products = database_dostavka.get_all_products()

    for product in products:
        kb.add(product)

    return kb
