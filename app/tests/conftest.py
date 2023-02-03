import pytest
from flaskr import create_app
from flaskr.db import Database


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def test_db():
    conn = Database(test=True)

    yield conn

    conn.clear_messages_table()
    conn.clear_names_table()
    conn.close()
