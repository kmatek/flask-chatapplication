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


def test_saving_name(test_db):
    """Test saving user's names."""
    conn = test_db
    names = ['test1', 'test2', 'test3']

    for name in names:
        conn.save_name(name)

    for name in names:
        assert conn.save_name(name) == False # noqa


def test_removing_name(test_db):
    """Test removing names from table."""
    conn = test_db
    names = ['test1', 'test2', 'test3']

    for name in names:
        conn.save_name(name)

    for name in names:
        conn.remove_name(name)

    conn.cursor.execute("SELECT count(name) FROM LoggedUsers;")
    result = conn.cursor.fetchall()

    assert result[0] == (0,)
