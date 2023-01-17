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
def runner(app):
    return app.test_cli_runner()


@pytest.fixture(scope='module')
def test_db():
    conn = Database(test=True)

    yield conn

    conn.clear_table()
    conn.close()
