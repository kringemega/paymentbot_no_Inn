from telebot import types
import telebot
import os
import threading


API_TOKEN = '7916764974:AAHJ7fxu0eFWgVgJMJsjC9k5bqth2W0yb4s'  # Замените на ваш актуальный токен бота
bot = telebot.TeleBot(API_TOKEN)
OWNER_ID = 1444450406  # Замените на ID владельца



print("▪   ▐ ▄ .▄▄ ·  ▄▄▄·  ▐ ▄ ▄▄▄ . ▄▄▄· ▄▄▄·  ▄· ▄▌• ▌ ▄ ·. ▄▄▄ . ▐ ▄ ▄▄▄▄▄.▄▄ · ")
print("██ •█▌▐█▐█ ▀. ▐█ ▀█ •█▌▐█▀▄.▀·▐█ ▄█▐█ ▀█ ▐█▪██▌·██ ▐███▪▀▄.▀·•█▌▐█•██  ▐█ ▀.")
print("▐█·▐█▐▐▌▄▀▀▀█▄▄█▀▀█ ▐█▐▐▌▐▀▀▪▄ ██▀·▄█▀▀█ ▐█▌▐█▪▐█ ▌▐▌▐█·▐▀▀▪▄▐█▐▐▌ ▐█.▪▄▀▀▀█▄")
print("▐█▌██▐█▌▐█▄▪▐█▐█▪ ▐▌██▐█▌▐█▄▄▌▐█▪·•▐█▪ ▐▌ ▐█▀·.██ ██▌▐█▌▐█▄▄▌██▐█▌ ▐█▌·▐█▄▪▐█")
print("▐█▌██▐█▌▐█▄▪▐█▐█▪ ▐▌██▐█▌▐█▄▄▌▐█▪·•▐█▪ ▐▌ ▐█▀·.██ ██▌▐█▌▐█▄▄▌██▐█▌ ▐█▌·▐█▄▪▐█")
print("▀▀▀▀▀ █▪ ▀▀▀▀  ▀  ▀ ▀▀ █▪ ▀▀▀ .▀    ▀  ▀   ▀ • ▀▀  █▪▀▀▀ ▀▀▀ ▀▀ █▪ ▀▀▀  ▀▀▀▀ ")
# Словари для хранения информации о пользователях
subscribed_users = {}
user_language = {}

def add_user_to_file(user_id):
    with open("sub.txt", "a") as f:
        f.write(f"(ID: {user_id})\n")
def console_commands():
    while True:
        command = input("Введите команду (give ID или revoke ID): ")
        parts = command.split()

        if len(parts) < 2:
            print("Пожалуйста, укажите команду и ID пользователя.")
            continue

        action = parts[0]
        user_id = parts[1]

        if not user_id.isdigit():
            print("Пожалуйста, укажите корректный ID пользователя.")
            continue

        user_id = int(user_id)

        if action == "give":
            if user_id not in subscribed_users:
                subscribed_users[user_id] = True
                bot.send_message(user_id, "✅ Ваша подписка была выдана! Теперь у вас есть доступ к команде /sub.")
                print(f"Подписка выдана пользователю с ID {user_id}.")
                write_subscribers_to_file()  # Сохраняем изменения в файл
            else:
                print(f"Пользователь с ID {user_id} уже подписан.")

        elif action == "revoke":
            if user_id in subscribed_users:
                del subscribed_users[user_id]
                bot.send_message(user_id, "❌ Ваша подписка была отозвана." if user_language.get(user_id,
                                                                                                "ru") == "ru" else "❌ Your subscription has been revoked.")
                print(f"Подписка у пользователя с ID {user_id} была отозвана.")
                write_subscribers_to_file()  # Сохраняем изменения в файл
            else:
                print(f"Пользователь с ID {user_id} не имеет активной подписки.")
        else:
            print("Неизвестная команда. Используйте 'give ID' или 'revoke ID'.")


def write_subscribers_to_file():
    with open("sub.txt", "w") as f:
        for user_id in subscribed_users:
            user_name = bot.get_chat(user_id).first_name
            f.write(f"(ID: {user_id})\n")

# Функция для загрузки подписчиков из файла
def load_subscribers_from_file():
    if os.path.exists("sub.txt"):
        with open("sub.txt", "r") as f:
            for line in f:
                if "ID:" in line:
                    user_id = int(line.split("ID: ")[1].strip().strip(")"))
                    subscribed_users[user_id] = True
                    bot.send_message(user_id, "⚠️ Бот перезагрузился подписка восстановлена.")

# Функция для выбора языка
@bot.message_handler(commands=['start'])
def choose_language(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_russian = types.KeyboardButton("Русский")
    item_english = types.KeyboardButton("English")
    markup.add(item_russian, item_english)
    bot.send_message(message.chat.id, "Choose your language / Выберите язык:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["Русский", "English"])
def set_language(message):
    if message.text == "Русский":
        user_language[message.chat.id] = "ru"
        bot.send_message(message.chat.id, "Вы выбрали русский язык.")
    elif message.text == "English":
        user_language[message.chat.id] = "en"
        bot.send_message(message.chat.id, "You selected English.")
    show_main_menu(message)

def show_main_menu(message):
    lang = user_language.get(message.chat.id, "ru")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Товары" if lang == "ru" else "Products")
    markup.add(item1)
    welcome_text = (
        "Добро пожаловать, {0}! Пока тут ещё недоделана хорошая система оплаты, но присутствует подписка на все товары, она стоит 100₽ | 1$"
        if lang == "ru" else
        "Welcome, {0}! The payment system is still in development, but a subscription for all products is available for 100₽ | 1$"
    )
    bot.send_message(message.chat.id, welcome_text.format(message.from_user.first_name), parse_mode='html', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["Товары", "Products"])
def show_categories(message):
    lang = user_language.get(message.chat.id, "ru")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_minecraft = types.KeyboardButton("Minecraft")
    item_cs2 = types.KeyboardButton("CS2")
    item_back = types.KeyboardButton("Назад" if lang == "ru" else "Back")
    markup.add(item_minecraft, item_cs2, item_back)

    bot.send_message(message.chat.id, "Выберите категорию товаров:" if lang == "ru" else "Choose a product category:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Minecraft")
def show_minecraft_products(message):
    lang = user_language.get(message.chat.id, "ru")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_back = types.KeyboardButton("Назад" if lang == "ru" else "Back")
    markup.add(item_back)

    product_list = (
        "Minecraft товары:\n- Arbuz.cc:2.0:funtime - 70₽\n- Nursultan:Alpha:Funtime - 90₽\nДля покупки используйте /buy"
        if lang == "ru" else
        "Minecraft products:\n- Arbuz.cc:2.0:funtime - 70₽\n- Nursultan:Alpha:Funtime - 90₽\nnUse /buy to purchase"
    )
    bot.send_message(message.chat.id, product_list, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "CS2")
def show_cs2_products(message):
    lang = user_language.get(message.chat.id, "ru")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_back = types.KeyboardButton("Назад" if lang == "ru" else "Back")
    markup.add(item_back)

    product_list = (
        "CS2 товары:\n- Midnight:Semirage - 71₽\n- Nixware - 95₽\nДля покупки используйте /buy"
        if lang == "ru" else
        "CS2 products:\n- Midnight:Semirage - 71₽\n- Nixware - 95₽\nUse /buy to purchase"
    )
    bot.send_message(message.chat.id, product_list, reply_markup=markup)

@bot.message_handler(commands=['buy'])
def button(message):
    lang = user_language.get(message.chat.id, "ru")
    markup = types.InlineKeyboardMarkup(row_width=2)
    item = types.InlineKeyboardButton('Boosty', callback_data='Boosty2')
    item_back = types.InlineKeyboardButton("Назад" if lang == "ru" else "Back", callback_data='back_to_products')
    markup.add(item, item_back)

    bot.send_message(message.chat.id, 'Способ оплаты\nЕсли оплатили, то используйте /verify' if lang == "ru" else 'Payment method\nIf you have paid, use /verify', reply_markup=markup)

@bot.message_handler(commands=["verify"])
def button2(message):
    lang = user_language.get(message.chat.id, "ru")
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("Я оплатил ✅" if lang == "ru" else "I paid ✅", callback_data="vers")
    item_back = types.InlineKeyboardButton("Назад" if lang == "ru" else "Back", callback_data="back_to_buy")
    markup.add(item1, item_back)

    verify_text = (
        '💰 Оплатили?\nОтправьте квитанцию об оплате: скриншот или фото.\nПрайс подписки 100₽ | 1$'
        if lang == "ru" else
        '💰 Did you pay?\nSend a receipt: screenshot or photo.\nSubscription price: 100₽ | 1$'
    )
    bot.send_message(message.chat.id, verify_text, reply_markup=markup)

@bot.message_handler(content_types=["photo"])
def handle_receipt(message):
    file_id = message.photo[-1].file_id
    keyboard = types.InlineKeyboardMarkup()
    accept_button = types.InlineKeyboardButton("✅Принять", callback_data=f"accept_{message.chat.id}")
    reject_button = types.InlineKeyboardButton("❌Отклонить", callback_data=f"reject_{message.chat.id}")
    keyboard.add(accept_button, reject_button)

    bot.send_photo(OWNER_ID, file_id, reply_markup=keyboard)
    lang = user_language.get(message.chat.id, "ru")
    bot.send_message(message.chat.id, "Квитанция получена. Мы проверим и свяжемся с вами." if lang == "ru" else "Receipt received. We will review and contact you.")

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    lang = user_language.get(call.message.chat.id, "ru")
    if call.message:
        if call.data == "vers":
            bot.send_message(call.message.chat.id, "Пришлите скриншот квитанции, чтобы завершить покупку." if lang == "ru" else "Send a screenshot of the receipt to complete the purchase.")
        elif call.data == 'Boosty2':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='⚠️Нужно отправить точную сумму по ссылке: https://boosty.to/krinj/donate. Оплатили? /verify' if lang == "ru" else 'Send the exact amount via the link: https://boosty.to/krinj/donate. Paid? /verify')
        elif call.data == 'back_to_products':
            show_categories(call.message)
        elif call.data == 'back_to_buy':
            button(call.message)
        elif call.data.startswith("accept_"):
            buyer_id = int(call.data.split("_")[1])
            subscribed_users[buyer_id] = True
            bot.send_message(buyer_id,
                             "✅Оплата подтверждена! Теперь у вас есть доступ к команде /sub." if lang == "ru" else "✅ Payment confirmed! Now you have access to the /sub command.")
            bot.send_message(OWNER_ID, "✅ Оплата принята." if lang == "ru" else "✅ Payment accepted.")

            add_user_to_file(buyer_id)  # Add the user to sub.txt after payment confirmation

        elif call.data.startswith("reject_"):
            buyer_id = int(call.data.split("_")[1])
            bot.send_message(buyer_id, "❌Оплата отклонена. Пожалуйста, свяжитесь с поддержкой." if lang == "ru" else "❌ Payment rejected. Please contact support.")
            bot.send_message(OWNER_ID, "❌ Оплата отклонена." if lang == "ru" else "❌ Payment rejected.")

@bot.message_handler(commands=["sub"])
def subscription_access(message):
    lang = user_language.get(message.chat.id, "ru")
    if subscribed_users.get(message.chat.id, False):
        bot.send_message(message.chat.id, "Ссылка на товары: https://mega.nz/folder/vZUG2ZYS#tXoC2SBmeh1d9LItvvhTmg;Ключ - tXoC2SBmeh1d9LItvvhTmg" if lang == "ru" else "Link to products: https://mega.nz")
    else:
      bot.send_message(message.chat.id, "❌У вас нет доступа к этой команде. Пожалуйста, оформите подписку.")
# Команда для выдачи подписки
@bot.message_handler(commands=['give'])
def give_subscription(message):
    if message.chat.id != OWNER_ID:
        return

    # Проверяем, что ID пользователя указан
    user_id = message.text.split(' ')[1] if len(message.text.split(' ')) > 1 else None
    if user_id and user_id.isdigit():
        user_id = int(user_id)
        subscribed_users[user_id] = True  # Добавляем пользователя в список с подпиской
        bot.send_message(user_id, "✅ Ваша подписка была выдана! Теперь у вас есть доступ к команде /sub.")
        bot.send_message(OWNER_ID, f"Подписка выдана пользователю с ID {user_id}.")
        write_subscribers_to_file()  # Записываем подписчиков в файл
    else:
        bot.send_message(OWNER_ID, "Пожалуйста, укажите корректный ID пользователя.")

# Команда для просмотра списка подписчиков (доступна только владельцу)
@bot.message_handler(commands=['list'])
def list_subscribers(message):
    if message.chat.id != OWNER_ID:
        return

    if not subscribed_users:
        bot.send_message(OWNER_ID, "На данный момент нет активных подписчиков." if user_language.get(message.chat.id, "ru") == "ru" else "There are no active subscribers at the moment.")
        return

    for user_id in subscribed_users:
        user_name = bot.get_chat(user_id).first_name or "отсутствует"
        keyboard = types.InlineKeyboardMarkup()
        revoke_button = types.InlineKeyboardButton("Забрать подписку" if user_language.get(message.chat.id, "ru") == "ru" else "Revoke subscription", callback_data=f"revoke_{user_id}")
        keyboard.add(revoke_button)
        bot.send_message(OWNER_ID, f"Пользователь: {user_name} (ID: {user_id})" if user_language.get(message.chat.id, "ru") == "ru" else f"User: {user_name} (ID: {user_id})", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith("revoke_"))
def revoke_subscription(call):
    if call.message.chat.id != OWNER_ID:
        return

    user_id = int(call.data.split("_")[1])
    if user_id in subscribed_users:
        del subscribed_users[user_id]
        bot.send_message(user_id, "❌ Ваша подписка была отозвана." if user_language.get(user_id, "ru") == "ru" else "❌ Your subscription has been revoked.")
        bot.send_message(OWNER_ID, f"Подписка у пользователя с ID {user_id} была отозвана." if user_language.get(call.message.chat.id, "ru") == "ru" else f"Subscription for user ID {user_id} has been revoked.")
        write_subscribers_to_file()  # Записываем подписчиков в файл

threading.Thread(target=console_commands, daemon=True).start()

load_subscribers_from_file()

bot.polling(none_stop=True)

