import telebot
from telebot import types

import database_dostavka
import buttons


# Подключение бота
bot = telebot.TeleBot('5450270265:AAF-jeIKwLYON-yLWnrBUxv-v5d1ru0uchg')


# print(bot.get_chat('@gaga').id)  # Получить канала или группы


# Обработчик команды старт
@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id

    checker = database_dostavka.check_user(user_id)

    if checker:
        bot.send_message(user_id, text='Выберите нужный для вас пункт', reply_markup=buttons.main_menu_buttons())

    else:
        bot.send_message(user_id, 'Добро пожаловать!\nОтправьте своя имя')
        bot.register_next_step_handler(message, get_name)


# Этап получения имени
def get_name(message):
    user_id = message.from_user.id
    user_name = message.text

    bot.send_message(user_id, 'Отправьте номер', reply_markup=buttons.phone_number_button())
    bot.register_next_step_handler(message, get_number, user_name)


# Этап получения номера
def get_number(message, user_name):
    user_id = message.from_user.id

    if message.contact:
        phone_number = message.contact.phone_number

        bot.send_message(user_id, 'Отправьте локацию', reply_markup=buttons.location_button())
        bot.register_next_step_handler(message, get_location, user_name, phone_number)
    else:
        bot.send_message(user_id, 'Отправьте номер используя кнопку')
        bot.register_next_step_handler(message, get_number, user_name)


# Этап получение локации
def get_location(message, user_name, phone_number):
    user_id = message.from_user.id

    if message.location:  # Если отправил локацию
        user_location = (message.location.latitude, message.location.longitude)

        # Регистрируем в базу
        database_dostavka.regist_user(user_id, phone_number, user_name, user_location[1], user_location[0])

        bot.send_message(user_id, 'Успешно зарегистрировали\nВыберите нужный для вас пункт',
                         reply_markup=buttons.main_menu_buttons())

    else:
        bot.send_message(user_id, 'Отправьте локацию используя кнопку')
        bot.register_next_step_handler(message, get_location, user_name, phone_number)


# Админ панель #
@bot.message_handler(commands=['admin'])
def admin_side(message):
    admin_id = 777322005

    if admin_id == message.from_user.id:
        bot.send_message(admin_id, 'Выберите нужный пункт', reply_markup=buttons.admin_product_buttons())


def get_product_name(message):
    product_name = message.text
    admin_id = 777322005

    bot.send_message(admin_id, 'Введите цену продукта')
    bot.register_next_step_handler(message, get_product_price, product_name)


def get_product_price(message, product_name):
    product_price = message.text
    admin_id = 777322005

    bot.send_message(admin_id, 'Введите описание продукта')
    bot.register_next_step_handler(message, get_product_description, product_name, product_price)


def get_product_description(message, product_name, product_price):
    product_description = message.text
    admin_id = 777322005

    bot.send_message(admin_id, 'Отправьте фото')
    bot.register_next_step_handler(message, get_product_photo, product_name, product_price, product_description)


def get_product_photo(message, product_name, product_price, product_description):
    admin_id = 777322005

    if message.photo:
        database_dostavka.create_product(product_name, product_price, product_description, message.photo[-1].file_id)
        bot.send_message(admin_id, 'Продукт успешно добавлен', reply_markup=buttons.admin_product_buttons())
    else:
        bot.send_message(admin_id, 'Отправьте другой')
        bot.register_next_step_handler(message, get_product_photo, product_name, product_price, product_description)


# Удаление продукта
def delete_exact_product(message):
    admin_id = 777322005
    product_name = message.text
    database_dostavka.delete_exact_product(product_name)
    bot.send_message(admin_id, 'Продукт успешно удален', reply_markup=buttons.admin_product_buttons())


# Изменения цены продукта #
def get_product_name_to_update(message):
    admin_id = 777322005
    product_name = message.text
    bot.send_message(admin_id, 'Введите новыю цену')
    bot.register_next_step_handler(message, update_exact_product_price, product_name)


def update_exact_product_price(message, product_name):
    admin_id = 777322005
    product_new_price = message.text
    database_dostavka.update_price_of_product(product_name, product_new_price)
    bot.send_message(admin_id, 'Цена продукта успешно изменена', reply_markup=buttons.admin_product_buttons())
################################################################


# Обработчик
@bot.message_handler(content_types=['text'])
def text_messages(message):
    user_id = message.from_user.id
    admin_id = 777322005

    if admin_id == message.from_user.id:
        if message.text == 'Добавить продукт':
            bot.send_message(admin_id, 'Введите имя продукта', reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, get_product_name)

        elif message.text == 'Удалить продукт':
            bot.send_message(admin_id, 'Выберите продукт которого хотите удалить',
                             reply_markup=buttons.admin_all_product_button())

            bot.register_next_step_handler(message, delete_exact_product)

        elif message.text == 'Изменить цену продукта':
            bot.send_message(admin_id, 'Выберите продукт которого хотите изменить цену',
                             reply_markup=buttons.admin_all_product_button())

            bot.register_next_step_handler(message, get_product_name_to_update)

    if message.text == 'Каталог':
        bot.send_message(user_id, 'Выберите товар', reply_markup=buttons.products_button())

    elif message.text == 'Связаться с нами':
        bot.send_message(user_id, 'Наши контакты:\n+998900000000')

    elif message.text == 'Основное меню':
        bot.send_message(user_id, 'Выберите пункт', reply_markup=buttons.main_menu_buttons())

    elif message.text == 'Корзина':
        user_cart = database_dostavka.get_exact_user_cart(user_id)

        # Формирование сообщения для вывода всей картины
        if user_cart != '':
            full_message = 'Ваша корзина:\n\n'

            for cart in user_cart:
                if user_cart != '':
                    full_message += f'{cart[1]} : {cart[2]}шт : {cart[-1]} сум\n'
                    bot.send_message(user_id, full_message, reply_markup=buttons.basket_button())
        else:
            bot.send_message(user_id, 'Корзина пустая')

    elif message.text == 'Оформить заказ':
        bot.send_message(user_id, 'Оформим заказ?', reply_markup=buttons.confirm_order_button())
        bot.register_next_step_handler(message, get_accept)

    elif message.text in database_dostavka.get_all_products():
        user_product = message.text

        current_product = database_dostavka.get_exact_product(user_product)

        # Отправка инфо и фото товара
        bot.send_photo(user_id, photo=current_product[4],
                       caption=f"{current_product[3]}\n\n{current_product[2]}")

        bot.send_message(user_id, 'Выберите количиство', reply_markup=buttons.product_count_button())
        bot.register_next_step_handler(message, get_product_count, user_product)


# Этап получения количиства товара
def get_product_count(message, user_product):
    user_id = message.from_user.id

    if message.text.isnumeric():  # Если сообщение отправленно в числовом виде
        product_count = int(message.text)

        # Добавим в корзину пользователя
        database_dostavka.create_user_cart(user_id, user_product, product_count)

        bot.send_message(user_id, 'Продукты добавлен в корзину', reply_markup=buttons.products_button())

    else:
        bot.send_message(user_id, 'Выберите количество используя кнопки')
        bot.register_next_step_handler(message, get_product_count, user_product)


def get_accept(message):
    user_id = message.from_user.id

    if message.text == 'Потвердить':
        user_products = database_dostavka.get_exact_user_cart(user_id)
        full_order_message = 'Ваш заказ:\n\n'
        full_admin_message = f'Новый заказ: {user_id}\n\n'
        total_sum = 0

        for order in user_products:
            # Для пользователя
            full_order_message += f'{order[1]} : {order[2]}шт : {order[-1]}сум\n'
            #  Для админа
            full_admin_message += f'{order[1]} : {order[2]}шт : {order[-1]}сум\n'
            # Подсчет общей суммы
            total_sum += order[-1]

        full_order_message += f'\nИтог: {total_sum} \nОформлен'  # Для пользователя
        full_admin_message += f'\nИтог: {total_sum}'  # Для админа

        bot.send_message(user_id, full_order_message, reply_markup=buttons.main_menu_buttons())
        bot.send_message(777322005, full_admin_message)

        database_dostavka.clear_user_cart(user_id)

    else:
        database_dostavka.clear_user_cart(user_id)
        bot.send_message(user_id, 'Заказ отменен', reply_markup=buttons.main_menu_buttons())


# Запуск бота
bot.polling()
