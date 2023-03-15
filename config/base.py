import logging
import os


class BaseConfig:
    LOGGING_LEVEL = logging.INFO
    mysql_pwd = os.getenv("MYSQL_PWD", "123456")
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:{mysql_pwd}@127.0.0.1/catalog"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
