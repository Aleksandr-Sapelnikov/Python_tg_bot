import telebot
import config
from telebot.handler_backends import State, StatesGroup
from telebot import custom_filters
from telebot.storage import StateMemoryStorage


class User:
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

    @classmethod
    def add_user(cls, user_id, user):
        cls.all_users[user_id] = user

    @classmethod
    def get_user(cls, user_id):
        if user_id in cls.all_users:
            return cls.all_users[user_id]
        User(user_id=user_id)
        return cls.all_users[user_id]


class LowState(StatesGroup):
    count_photo = State()
    photo = State()
    city = State()
    city_id = State()
    start_date = State()
    end_date = State()
    adults = State()
    resultsSize = State()
    answer = State()


class HighState(StatesGroup):
    city = State()
    city_id = State()
    start_date = State()
    end_date = State()
    adults = State()
    resultsSize = State()
    answer = State()


class BestState(StatesGroup):
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