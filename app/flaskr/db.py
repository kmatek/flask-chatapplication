import os
from datetime import datetime
from typing import List, Tuple, Dict, Any
import psycopg2

JsonDict = Dict[str, Any]


class Database:
    """Databse config for an application."""
    def __init__(self, test: bool = False):
        self.conn = False

        try:
            if not test:
                self.conn = psycopg2.connect(
                    host=os.environ.get('DB_HOST'),
                    database=os.environ.get('DB_NAME'),
                    user=os.environ.get('DB_USER'),
                    password=os.environ.get('DB_PASSWORD'))
            else:
                self.conn = psycopg2.connect(
                    host='test_db',
                    database='test_db',
                    user='test_user',
                    password='test_password')
        except (Exception, psycopg2.DatabaseError) as e:
            raise e

        self.cursor = self.conn.cursor()
        self._create_table()

    def close(self) -> None:
        """Close connection to the database."""
        self.conn.close()

    def _create_table(self) -> None:
        """Create new a database table if doesnt exist."""
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS Messages
            (id SERIAL PRIMARY KEY, name varchar, content varchar, time timestamp)""") # noqa
        self.conn.commit()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS LoggedUsers (name varchar UNIQUE)""") # noqa
        self.conn.commit()

    def save_message(self, json: JsonDict) -> None:
        """Save message in the table."""
        message = json.get('message')
        name = json.get('name')
        date = datetime.strptime(json.get('date'), "%d.%m.%Y, %H:%M")

        self.cursor.execute(
            """INSERT INTO Messages (name, content, time)
            VALUES (%s, %s, %s)""",
            (name, message, date))
        self.conn.commit()

    def get_messages(self, limit: int = 100) -> List[Tuple]:
        """Return all messages."""
        self.cursor.execute("SELECT * FROM Messages ORDER BY time LIMIT %s;", (limit,)) # noqa
        result = self.cursor.fetchall()[:limit]
        return result

    def clear_messages_table(self) -> None:
        """Helper method for tests."""
        self.cursor.execute('TRUNCATE TABLE Messages;')
        self.conn.commit()

    def save_name(self, name: str) -> bool:
        """Save the name of the user currently is using chat"""
        # Check that name is already used
        try:
            self.cursor.execute(
                """INSERT INTO LoggedUsers (name) VALUES (%s);""", (name,))
            self.conn.commit()
            return True
        except psycopg2.errors.UniqueViolation:
            self.conn.rollback()
            return False

    def remove_name(self, name: str) -> None:
        """Remove user's name when leaving the chat room."""
        # Check that name is not deleted
        self.cursor.execute("DELETE FROM LoggedUsers WHERE name LIKE %s", (name,)) # noqa
        self.conn.commit()

    def clear_names_table(self) -> None:
        """Helper method for tests."""
        self.cursor.execute('TRUNCATE TABLE LoggedUsers;')
        self.conn.commit()
