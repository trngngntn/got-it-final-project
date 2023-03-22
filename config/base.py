import logging
import os


class BaseConfig:
    LOGGING_LEVEL = logging.INFO
    MYSQL_PWD = os.getenv("MYSQL_PWD", "123456")
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:{MYSQL_PWD}@127.0.0.1/catalog"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = "66b49b551a0c0fe0"
    JWT_ALGO = "HS256"
    JWT_TIMEOUT_SECONDS = 5 * 60

    HASH_ALGO = "sha256"
    HASH_ITERS = 100_000
    SALT_BYTE_LENGTH = 8
    SALT_HEX_LENGTH = SALT_BYTE_LENGTH * 2

    PATTERN_PWD = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d).{6,}$"

    PAGINATION_MAX_ITEMS = 20
