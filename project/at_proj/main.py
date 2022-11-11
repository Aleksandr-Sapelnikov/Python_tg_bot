import loader
import core_commands
import lowprice
import highprice
import bestdeal
from datetime import datetime


if __name__ == '__main__':
    @loader.bot.message_handler(state=None, commands=['start'])
    def start(message):
        user = loader.User.get_user(message.from_user.id)
        cut_time = datetime.now().strftime('%d.%m.%y %H:%M:%S')
        user.history[cut_time] = message.text
        sent = loader.bot.send_message(message.from_user.id, f"Привет, "
                                                             f"{message.from_user.first_name} "
                                                             f"{message.from_user.username} "
                                                             f"{message.from_user.last_name}!"
                                                             f"\nВведи одну из команд для продолжения")


    @loader.bot.message_handler(state=None, commands=['help'])
    def start(message):
        user = loader.User.get_user(message.from_user.id)
        cut_time = datetime.now().strftime('%d.%m.%y %H:%M:%S')
        user.history[cut_time] = message.text
        sent = loader.bot.send_message(message.from_user.id, f"Список команд бота:"
                                                             f"\n/start - Приветствие"
                                                             f"\n/help - Справка"
                                                             f"\n/lowprice - Поиск бюджетных отелей"
                                                             f"\n/highprice - Поиск лучших отелей"
                                                             f"\n/bestdeal - Поиск с настройками цены"
                                                             f"\n/history - История поиска")


    @loader.bot.message_handler(state=None, commands=['lowprice'])
    def start(message):
        user = loader.User.get_user(message.from_user.id)
        cut_time = datetime.now().strftime('%d.%m.%y %H:%M:%S')
        user.history[cut_time] = message.text
        sent = loader.bot.send_message(message.from_user.id, "Какой город?")
        print(sent.text)
        user.lowprice = True
        loader.bot.set_state(user_id=message.from_user.id, state=loader.CommandState.city, chat_id=message.chat.id)
        # loader.bot.set_state(user_id=message.from_user.id, state=loader.LowState.city, chat_id=message.chat.id)


    @loader.bot.message_handler(state=None, commands=['highprice'])
    def start(message):
        user = loader.User.get_user(message.from_user.id)
        cut_time = datetime.now().strftime('%d.%m.%y %H:%M:%S')
        user.history[cut_time] = message.text
        sent = loader.bot.send_message(message.from_user.id, "Какой город?")
        print(sent.text)
        user.highprice = True
        loader.bot.set_state(user_id=message.from_user.id, state=loader.CommandState.city, chat_id=message.chat.id)
        # loader.bot.set_state(user_id=message.from_user.id, state=loader.HighState.city, chat_id=message.chat.id)

    # Сейчас ищет от 300 до 2000$ и 5 звезд и конечно выдает все около 300

    @loader.bot.message_handler(state=None, commands=['bestdeal'])
    def start(message):
        user = loader.User.get_user(message.from_user.id)
        cut_time = datetime.now().strftime('%d.%m.%y %H:%M:%S')
        user.history[cut_time] = message.text
        sent = loader.bot.send_message(message.from_user.id, "Какой город?")
        print(sent.text)
        user.bestdeal = True
        loader.bot.set_state(user_id=message.from_user.id, state=loader.CommandState.city, chat_id=message.chat.id)
        # loader.bot.set_state(user_id=message.from_user.id, state=loader.BestState.city, chat_id=message.chat.id)


    @loader.bot.message_handler(state=None, commands=['history'])  # Если писать сообщения больше 1 в сек, то будут проблемы
    def get_history(message):
        user = loader.User.get_user(message.from_user.id)
        # cut_time = datetime.now().strftime('%d.%m.%y %H:%M:%S')
        # user.history[cut_time] = message.text
        ans = ''
        for i, j in user.history.items():
            ans += f'[{i}]: {j}\n'
        loader.bot.send_message(message.chat.id, ans)


    @loader.bot.message_handler(state=None, content_types=['text'])
    def start(message):
        if message.text.lower() == 'привет' or '/hello-world':
            loader.bot.send_message(message.from_user.id, 'Привет, я - PythonAttestatBot\nМожешь ввести '
                                                          '/help для просмотра списка команд')

    loader.bot.infinity_polling()
