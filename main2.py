from telebot import types
import telebot

API_TOKEN = '7916764974:AAHJ7fxu0eFWgVgJMJsjC9k5bqth2W0yb4s'  # Замените на ваш актуальный токен бота
bot = telebot.TeleBot(API_TOKEN)
OWNER_ID = 1444450406  # Замените на ID владельца

# Словарь для хранения пользователей с активной подпиской
subscribed_users = {}

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Товары")
    markup.add(item1)

    bot.send_message(
        message.chat.id,
        f"Добро пожаловать, {message.from_user.first_name}!Пока тут ещё недоделана хорошая система оплаты, но присутствует подписка на все товары , она стоит 100₽ | 1$",
        parse_mode='html', reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == "Товары")
def show_categories(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_minecraft = types.KeyboardButton("Minecraft")
    item_cs2 = types.KeyboardButton("CS2")
    item_back = types.KeyboardButton("Назад")
    markup.add(item_minecraft, item_cs2, item_back)

    bot.send_message(message.chat.id, "Выберите категорию товаров:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Minecraft")
def show_minecraft_products(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_back = types.KeyboardButton("Назад")
    markup.add(item_back)

    product_list = "Minecraft товары:\n- Продукт A - 70₽\n- Продукт B - 120₽\nДля покупки используйте /buy"
    bot.send_message(message.chat.id, product_list, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "CS2")
def show_cs2_products(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_back = types.KeyboardButton("Назад")
    markup.add(item_back)

    product_list = "CS2 товары:\n- Продукт C - 50₽\n- Продукт D - 100₽\nДля покупки используйте /buy"
    bot.send_message(message.chat.id, product_list, reply_markup=markup)

@bot.message_handler(commands=['buy'])
def button(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item = types.InlineKeyboardButton('Boosty', callback_data='Boosty2')
    item_back = types.InlineKeyboardButton('Назад', callback_data='back_to_products')
    markup.add(item, item_back)

    bot.send_message(message.chat.id, 'Способ оплаты\nЕсли оплатили, то используйте /verify', reply_markup=markup)

@bot.message_handler(commands=["verify"])
def button2(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("Я оплатил ✅", callback_data="vers")
    item_back = types.InlineKeyboardButton("Назад", callback_data="back_to_buy")
    markup.add(item1, item_back)

    bot.send_message(message.chat.id, '💰 Оплатили?\nОтправьте квитанцию об оплате: скриншот или фото.\nПрайс подписки 100₽ | 1$', reply_markup=markup)

@bot.message_handler(content_types=["photo"])
def handle_receipt(message):
    file_id = message.photo[-1].file_id
    keyboard = types.InlineKeyboardMarkup()
    accept_button = types.InlineKeyboardButton("✅Принять", callback_data=f"accept_{message.chat.id}")
    reject_button = types.InlineKeyboardButton("❌Отклонить", callback_data=f"reject_{message.chat.id}")
    keyboard.add(accept_button, reject_button)

    bot.send_photo(OWNER_ID, file_id, reply_markup=keyboard)
    bot.send_message(message.chat.id, "Квитанция получена. Мы проверим и свяжемся с вами.")

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data == "vers":
            bot.send_message(call.message.chat.id, "Пришлите скриншот квитанции, чтобы завершить покупку.")
        elif call.data == 'Boosty2':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Нужно отправить точную сумму по ссылке: https://boosty.to/krinj/donate. Оплатили? /verify')
        elif call.data == 'back_to_products':
            show_categories(call.message)
        elif call.data == 'back_to_buy':
            button(call.message)
        elif call.data.startswith("accept_"):
            buyer_id = int(call.data.split("_")[1])
            subscribed_users[buyer_id] = True  # Добавляем пользователя в список с подпиской
            bot.send_message(buyer_id, "✅Оплата подтверждена! Теперь у вас есть доступ к команде /sub.")
            bot.send_message(OWNER_ID, "✅Оплата принята.")
        elif call.data.startswith("reject_"):
            buyer_id = int(call.data.split("_")[1])
            bot.send_message(buyer_id, "❌Оплата отклонена. Пожалуйста, свяжитесь с поддержкой.")
            bot.send_message(OWNER_ID, "❌Оплата отклонена.")

@bot.message_handler(func=lambda message: message.text == "Назад")
def back_to_start(message):
    welcome(message)

@bot.message_handler(commands=["sub"])
def subscription_access(message):
    if subscribed_users.get(message.chat.id, False):
        bot.send_message(message.chat.id, "Ссылка на товары: https://mega.nz")
    else:
        bot.send_message(message.chat.id, "У вас нет доступа к этой команде. Пожалуйста, оформите подписку.")

bot.polling(none_stop=True)
