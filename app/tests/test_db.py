from app.flaskr.db import Database
import psycopg2


def check_conn(connection):
    try:
        connection.conn.cursor
        return True
    except (Exception, psycopg2.DatabaseError):
        return False


def test_connection():
    db = Database()
    assert check_conn(db) == True  # noqa
