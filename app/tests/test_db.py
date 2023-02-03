from datetime import datetime


def test_connection(test_db):
    """Tests databse connection is successfuly."""
    conn = test_db

    assert bool(conn) == True  # noqa


def test_creating_table_and_saving_message(test_db):
    """Tests creating table while initial database."""
    conn = test_db
    # Save message
    data = {
        'message': 'test',
        'name': 'test',
        'date': '1.01.2023, 12:00'
    }
    conn.save_message(data)
    conn.cursor.execute("SELECT * FROM Messages;")

    result = conn.cursor.fetchall()

    assert type(result[0][3]) == datetime
    assert len(result) == 1
