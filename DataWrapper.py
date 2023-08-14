import sqlite3
import secrets
import string
import threading

class DataWrapper:
    def __init__(self, db_file):
        self.db_file = db_file
        self.lock = threading.Lock()

    def create_table(self):
        connection = self._get_connection()
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS data (
                id TEXT,
                data TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        connection.commit()
        connection.close()

    def _get_connection(self):
        return sqlite3.connect(self.db_file)

    def generate_random_id(self, length=8):
        characters = string.ascii_letters + string.digits
        return ''.join(secrets.choice(characters) for _ in range(length))

    def insert_data(self, data):
        random_id = self.generate_random_id()
        connection = self._get_connection()
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO data (id, data) VALUES (?, ?);
        ''', (random_id, data))
        connection.commit()
        connection.close()
        return random_id

    def query_by_id(self, id):
        connection = self._get_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM data WHERE id = ?', (id,))
        result = cursor.fetchone()
        connection.close()
        if result:
            return {
                'id': result[0],
                'data': result[1],
                'created_at': result[2]
            }
        else:
            return None

