import telebot
# from commands import lowprice
#
from telebot.types import BotCommand
import config
from api import search_city_id
from telebot.handler_backends import State, StatesGroup
from telebot import custom_filters
from telebot.storage import StateMemoryStorage

# bot = telebot.TeleBot(config.bot_token)


def set_default_commands(bot: telebot) -> None:
    bot.set_my_commands(
        [BotCommand(*i) for i in config.DEFAULT_COMMANDS])


class UserState(StatesGroup):
    city = State()
    city_id = State()
    start_date = State()
    end_date = State()


storage = StateMemoryStorage()
bot = telebot.TeleBot(config.bot_token, state_storage=storage)
bot.add_custom_filter(custom_filters.StateFilter(bot))



#
# def command_list(message):
#
#     @bot.message_handler(commands=['lowprice'])  # тут надо проверять команды?
#     def lowprice_message(message):
#         sent = bot.send_message(message.from_user.id, "Какой город?")
#         bot.register_next_step_handler(sent, search_city_id.get_city_id, 'lowprice')
#
#         # city_id = search_city_id.get_city_id(sent, 'lowprice')
#         # print(city_id)
#         data = bot.send_message(message.from_user.id, "Какая дата dd-mm-yy?")
#
#         # bot.register_next_step_handler(sent, lowprice.get_city_id)
#         # lowprice.lowprice_get(message)
#
#     @bot.message_handler(commands=['hightprice'])  # тут надо проверять команды?
#     def hightprice_message(message):
#         pass
#
#     def lowprice_continue(message, city_id):
#         pass
#         # bot.register_next_step_handler(sent, search_city_id.get_city_id, 'lowprice')


# @bot.message_handler(commands=['reg'])
# def lowprice_message(message):
#     bot.register_next_step_handler(message, lowprice.start)
#     # lowprice.lowprice_get(message)
#     print('опять reg')

# name = ''
# surname = ''
# age = 0
# @bot.message_handler(content_types=['text'])
# def start(message):
#     if message.text == '/reg':
#         sent = bot.send_message(message.from_user.id, "Как тебя зовут?")
#         bot.register_next_step_handler(sent, get_name) #  следующий шаг – функция get_name
#     else:
#         bot.send_message(message.from_user.id, 'Напиши /reg')
#
# def get_name(message): #получаем фамилию
#     global name
#     name = message.text
#     bot.send_message(message.from_user.id, 'Какая у тебя фамилия?')
#     bot.register_next_step_handler(message, get_surname)
#
# def get_surname(message):
#     global surname
#     surname = message.text
#     bot.send_message(message.from_user.id, 'Сколько тебе лет?')
#     bot.register_next_step_handler(message, get_age)
#
# def get_age(message):
#     global age
#     while age == 0: #проверяем что возраст изменился
#         try:
#              age = int(message.text) #проверяем, что возраст введен корректно
#         except Exception:
#              bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
#     bot.send_message(message.from_user.id, 'Тебе '+str(age)+' лет, тебя зовут '+name+' '+surname+'?')



# @bot.message_handler(commands=['button'])  # почему-то не работает (все перехватывает get_text_messages())
# def button_message(message):
#     markup = types.InlineKeyboardMarkup(row_width=2)  # Клавиатура в переменной
#     item1 = types.InlineKeyboardButton("Кнопка 1", callback_data='question_1')
#     item2 = types.InlineKeyboardButton("Кнопка 2", callback_data='goodbye')
#
#     markup.add(item1, item2)
#     bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)
#
#
# @bot.message_handler(content_types=['text'])
# def get_text_messages(message):
#     if message.text == "Привет":
#         bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
#
#     elif message.text == "/help":
#         bot.send_message(message.from_user.id, "Напиши привет")
#
#     elif message.text == "/lowprice":  # тут команда из условий
#         bot.send_message(message.from_user.id, "выбрали низкие цены", low_price(message))
#
#     # elif message.text == "/button":
#     #     markup = types.InlineKeyboardMarkup(row_width=2)  # Клавиатура в переменной
#     #     item1 = types.InlineKeyboardButton("Кнопка 1", callback_data='question_1')
#     #     item2 = types.InlineKeyboardButton("Кнопка 2", callback_data='goodbye')
#     #
#     #     markup.add(item1, item2)
#     #     bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)
#
#     else:
#         bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
#
#
# def low_price(message):
#     bot.send_message(message.from_user.id, "Тут как-то находится топ дешевых отелей в выбранном городе")

# bot.polling(none_stop=True, interval=0)

# @bot.message_handler(commands=['button'])  # почему-то не работает (все перехватывает get_text_messages())
# def button_message(message):
#     markup = types.InlineKeyboardMarkup(row_width=2)  # Клавиатура в переменной
#     item1 = types.InlineKeyboardButton("Кнопка 1", callback_data='question_1')
#     item2 = types.InlineKeyboardButton("Кнопка 2", callback_data='goodbye')
#
#     markup.add(item1, item2)
#     bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)


# @bot.callback_query_handler(func=lambda call: True)
# def callback(call):
#     if call.message:
#         if call.data == 'question_1':
#             bot.send_message(call.message.chat.id, 'Вы нажали кнопку 1')
#         elif call.data == 'goodbye':
#             bot.send_message(call.message.chat.id, 'Вы нажали кнопку 2')

#
if __name__ == '__main__':
    bot.infinity_polling()
