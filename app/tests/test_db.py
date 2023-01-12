from unittest.mock import patch
from flaskr.db import Database


@patch('flaskr.db.Database.get_connection')
def test_connection(patched_conn):
    try:
        db = Database()
    except Exception:
        pass
    patched_conn.return_value = True
    assert db.get_connection() == True  # noqa
