import loader
import core_commands
from datetime import datetime


if __name__ == '__main__':
    @loader.bot.message_handler(state=None, commands=['start'])
    def start(message):
        """
        Функция реагирующая на команду пользователя /start и выводит приветствие
        """
        user = loader.User.get_user(message.from_user.id)
        cut_time = datetime.now().strftime('%d.%m.%y %H:%M:%S')
        user.history[cut_time] = message.text
        answer = 'Привет, '
        if message.from_user.first_name:
            answer += message.from_user.first_name
        if message.from_user.username:
            answer += ' ' + message.from_user.username
        if message.from_user.last_name:
            answer += ' ' + message.from_user.last_name + '!'
        loader.bot.send_message(message.from_user.id, answer + '\nВведите /help для просмотра списка команд')


    @loader.bot.message_handler(state=None, commands=['help'])
    def start(message):
        """
        Функция реагирующая на команду пользователя /help и выводит список команд
        """
        user = loader.User.get_user(message.from_user.id)
        cut_time = datetime.now().strftime('%d.%m.%y %H:%M:%S')
        user.history[cut_time] = message.text
        loader.bot.send_message(message.from_user.id, f"Список команд бота:"
                                                             f"\n/start - Приветствие"
                                                             f"\n/help - Справка"
                                                             f"\n/lowprice - Поиск бюджетных отелей"
                                                             f"\n/highprice - Поиск лучших отелей"
                                                             f"\n/bestdeal - Поиск с настройками цены"
                                                             f"\n/history - История поиска")


    @loader.bot.message_handler(state=None, commands=['lowprice'])
    def start(message):
        """
        Функция реагирующая на команду пользователя /lowprice и запускающая цепочку команд спрашивая название города
        """
        user = loader.User.get_user(message.from_user.id)
        cut_time = datetime.now().strftime('%d.%m.%y %H:%M:%S')
        user.history[cut_time] = message.text
        sent = loader.bot.send_message(message.from_user.id, "Какой город?")
        print(sent.text)
        user.command = loader.Commands.LOWPRICE
        loader.bot.set_state(user_id=message.from_user.id, state=loader.CommandState.city, chat_id=message.chat.id)


    @loader.bot.message_handler(state=None, commands=['highprice'])
    def start(message):
        """
        Функция реагирующая на команду пользователя /highprice и запускающая цепочку команд спрашивая название города
        """
        user = loader.User.get_user(message.from_user.id)
        cut_time = datetime.now().strftime('%d.%m.%y %H:%M:%S')
        user.history[cut_time] = message.text
        sent = loader.bot.send_message(message.from_user.id, "Какой город?")
        print(sent.text)
        user.command = loader.Commands.HIGHPRICE
        loader.bot.set_state(user_id=message.from_user.id, state=loader.CommandState.city, chat_id=message.chat.id)


    @loader.bot.message_handler(state=None, commands=['bestdeal'])
    def start(message):
        """
        Функция реагирующая на команду пользователя /bestdeal и запускающая цепочку команд спрашивая название города
        """
        user = loader.User.get_user(message.from_user.id)
        cut_time = datetime.now().strftime('%d.%m.%y %H:%M:%S')
        user.history[cut_time] = message.text
        sent = loader.bot.send_message(message.from_user.id, "Какой город?")
        print(sent.text)
        user.command = loader.Commands.BESTDEAL
        loader.bot.set_state(user_id=message.from_user.id, state=loader.CommandState.city, chat_id=message.chat.id)


    @loader.bot.message_handler(state=None, commands=['history'])
    def get_history(message):
        """
        Функция реагирующая на команду пользователя /history и выводит историю поиска
        """
        user = loader.User.get_user(message.from_user.id)
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
