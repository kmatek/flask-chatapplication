from datetime import datetime


def test_connection(test_db):
    """Tests databse connection is successfuly."""
    conn = test_db

    assert bool(conn) == True  # noqa


def test_creating_table_and_saving_message(test_db):
    """Tests creating table while initial database."""
    conn = test_db
    # Save message
    conn.save_message('test', 'test_message', datetime.now())
    conn.cursor.execute("SELECT * FROM Messages;")

    result = conn.cursor.fetchall()

    assert len(result) == 1
