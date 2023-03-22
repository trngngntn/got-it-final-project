from .local import Config as _Config


class Config(_Config):
    TESTING = True
    # MYSQL_PWD = os.getenv("MYSQL_PWD", "Ntt123456")
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Ntt123456@127.0.0.1/catalog_test"
