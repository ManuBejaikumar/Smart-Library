from db_connection import get_connection
from models.Author import Author

class AuthorDAO:
    def __init__(self):
        self.conn = get_connection()

    def get_all(self):
        if not self.conn:
            return []
        with self.conn.cursor() as cur:
            cur.execute("SELECT author_id, name, bio FROM authors")
            return [Author(*row) for row in cur.fetchall()]

    def add_author(self, name, bio):
        if not self.conn:
            return False
        with self.conn.cursor() as cur:
            cur.execute("INSERT INTO authors (name, bio) VALUES (%s, %s)", (name, bio))
        self.conn.commit()
        return True