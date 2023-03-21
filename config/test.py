from .local import Config as _Config


class Config(_Config):
    TESTING = True
    # mysql_pwd = os.getenv("MYSQL_PWD", "123456")
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Ntt123456@127.0.0.1/catalog_test"
