import telebot

bot = telebot.TeleBot('Token_here')

options = ['Traditional', 'Eco', 'Woman-Safe', 'Driverless']

user_data = {}


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    markup.add(*options)
    bot.send_message(message.chat.id, "Choose one of the following options for taxi:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in options)
def handle_option(message):
    user_data[message.chat.id] = {'option': message.text}
    bot.send_message(message.chat.id, f'Choice: {message.text} taxi. \nNow send your current geo-location.')


@bot.message_handler(content_types=['location'])
def handle_location(message):
    chat_id = message.chat.id
    if 'location' not in user_data[chat_id]:
        user_data[chat_id]['location'] = message.location
        bot.send_message(chat_id, "Now send your desired geo-location.")

    else:
        user_data[chat_id]['desired_location'] = message.location
        bot.send_message(chat_id, "Processing your request...")
        bot.send_message(chat_id, "Proceed with the payment: https://fakepaymentlink.com")
        bot.send_message(chat_id, "Your request has been processed.")
        user_data.pop(chat_id)


bot.polling()
