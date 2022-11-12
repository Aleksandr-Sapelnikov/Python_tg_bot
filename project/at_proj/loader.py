import telebot
import config
from telebot.handler_backends import State, StatesGroup
from telebot import custom_filters
from telebot.storage import StateMemoryStorage
from enum import Enum


class Commands(Enum):
    """
    Класс для определения текущей команды
    """
    LOWPRICE = 1
    HIGHPRICE = 2
    BESTDEAL = 3


class User:
    """
    Пользовательский класс для хранения списка пользователей, а также их ответов на запросы бота
    """
    all_users = dict()

    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        User.add_user(user_id=user_id, user=self)
        self.property_dict: dict = {}
        self.hotel_list: list = list()
        self.city: str = ""
        self.hotel_id: str = ""
        self.history: dict = {}
        self.current_dict: dict = {}
        self.command = None

    @classmethod
    def add_user(cls, user_id, user):
        cls.all_users[user_id] = user

    @classmethod
    def get_user(cls, user_id):
        if user_id in cls.all_users:
            return cls.all_users[user_id]
        User(user_id=user_id)
        return cls.all_users[user_id]


class CommandState(StatesGroup):
    """
    Класс для хранения состояний. Используется в цепочке функций.
    """
    count_photo = State()
    photo = State()
    price = State()
    destination = State()
    city = State()
    city_id = State()
    start_date = State()
    end_date = State()
    adults = State()
    resultsSize = State()
    answer = State()


storage = StateMemoryStorage()
bot = telebot.TeleBot(config.bot_token, state_storage=storage)
bot.add_custom_filter(custom_filters.StateFilter(bot))