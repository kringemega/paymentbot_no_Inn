from telebot import types
import telebot
API_TOKEN = '7916764974:AAHJ7fxu0eFWgVgJMJsjC9k5bqth2W0yb4s' # Замените на токен вашего бота

bot = telebot.TeleBot(API_TOKEN)

OWNER_ID = 1444450406

@bot.message_handler(commands=['start'])
def welcome(message):
 markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
 item1 = types.KeyboardButton("Товары")
 markup.add(item1)

 bot.send_message(
  message.chat.id,
  f"Добро пожаловать, {message.from_user.first_name}!\n",
  parse_mode='html', reply_markup=markup
 )

@bot.message_handler(func=lambda message: message.text == "Товары")
def show_products(message):
 markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
 item_back = types.KeyboardButton("Назад")
 markup.add(item_back)

 texts = [
  "Midnight-Semirage"
 ]
 product_list = '\n'.join(texts)
 bot.send_message(message.chat.id, f"Доступные товары:\n{product_list}", reply_markup=markup)

# Обработка команды /buy
@bot.message_handler(commands=['buy'])
def button(message):
 markup = types.InlineKeyboardMarkup(row_width=2)
 item = types.InlineKeyboardButton('Boosty', callback_data='Boosty2')
 item_back = types.InlineKeyboardButton('Назад', callback_data='back_to_products')
 markup.add(item, item_back)

 bot.send_message(message.chat.id, 'Способ оплаты\nЕсли оплатили то /verify', reply_markup=markup)

# Обработка команды /verify
@bot.message_handler(commands=["verify"])
def button2(message):
 markup = types.InlineKeyboardMarkup(row_width=2)
 item1 = types.InlineKeyboardButton("Я оплатил ✅", callback_data="vers")
 item_back = types.InlineKeyboardButton("Назад", callback_data="back_to_buy")
 markup.add(item1, item_back)

 bot.send_message(message.chat.id, '💰 Оплатили?\nОтправьте боту квитанцию об оплате: скриншот или фото.', reply_markup=markup)

# Обработка фотографий (квитанции)
@bot.message_handler(content_types=["photo"])
def handle_receipt(message):
  # Получение фото
  file_id = message.photo[-1].file_id
  file = bot.get_file(file_id)


  bot.send_photo(OWNER_ID, file.file_path)

  # Создание клавиатуры
  keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
  keyboard.add(types.KeyboardButton('Принять'), types.KeyboardButton('Отклонить'))

  # Отправка клавиатуры владельцу
  bot.send_message(OWNER_ID, 'Принять или отклонить?', reply_markup=keyboard)

  bot.send_message(message.chat.id, "Квитанция получена. Мы проверим и свяжемся с вами.")

# Обработка всех callback-запросов
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
 if call.message:
  if call.data == "vers":
   bot.send_message(call.message.chat.id, "Пришлите скриншот квитанции, чтобы завершить покупку.")
  elif call.data == 'Boosty2':
   bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Нужно отправить именно ту сумму, за которую вы хотите получить товар')
  elif call.data == 'funpay2':
   bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Недоступно❌')
  elif call.data == 'back_to_products':
   show_products(call.message)
  elif call.data == 'back_to_buy':
   button(call.message)

# Обработка ответа от владельца бота
@bot.message_handler(func=lambda message: message.chat.id == OWNER_ID)
def handle_owner_response(message):
  if message.text == "Принять":
    bot.send_message(message.reply_to_message.forward_from.id, '123') # Отправляем "123" покупателю
  elif message.text == "Отклонить":
    pass # Ничего не делаем

# Обработка команды "Назад" в меню Товаров
@bot.message_handler(func=lambda message: message.text == "Назад")
def back_to_start(message):
 welcome(message)

bot.polling(none_stop=True)
