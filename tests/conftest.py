import os
import sys
from pathlib import Path

import pytest
from alembic.command import upgrade
from alembic.config import Config

from main import app as _app
from main import db

if os.getenv("ENVIRONMENT") != "test":
    print('Tests should be run with "ENVIRONMENT=test"')
    sys.exit(1)

ALEMBIC_CONFIG = (
    (Path(__file__) / ".." / ".." / "migrations" / "alembic.ini").resolve().as_posix()
)


@pytest.fixture(scope="session", autouse=True)
def app():
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope="session", autouse=True)
def recreate_database(app):
    db.reflect()
    db.drop_all()
    _config = Config(ALEMBIC_CONFIG)
    upgrade(_config, "heads")


@pytest.fixture(scope="function", autouse=True)
def session(recreate_database):
    from sqlalchemy.orm import sessionmaker

    connection = db.engine.connect()
    transaction = connection.begin()

    session_factory = sessionmaker(bind=connection)
    session = db.scoped_session(session_factory)

    db.session = session

    yield

    transaction.rollback()
    connection.close()
    session.close()


@pytest.fixture(scope="function", autouse=True)
def client(app, session):
    return app.test_client()
