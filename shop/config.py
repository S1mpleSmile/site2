from secrets import token_hex

class Config(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///shop.db"
    SECRET_KEY = token_hex(20)  # генерация секретного ключа в 16 СС
