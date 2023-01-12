import os
import psycopg2


class Database:
    """Databse config for an application."""
    def __init__(self):
        self.conn = False
        try:
            self.conn = psycopg2.connect(
                host=os.environ.get('DB_HOST'),
                database=os.environ.get('DB_NAME'),
                user=os.environ.get('DB_USER'),
                password=os.environ.get('DB_PASSWORD'))
        except (Exception, psycopg2.DatabaseError) as e:
            raise e

    def close(self) -> None:
        """Close connection to the database."""
        self.conn.close()
    
    def get_connection(self) -> bool:
        """Get connection status boolean."""
        return bool(self.conn)
