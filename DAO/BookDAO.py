from db_connection import get_connection
from models.Book import Book

class BookDAO:
    def __init__(self):
        self.conn = get_connection()

    def get_all(self):
        if not self.conn:
            return []
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT b.book_id, b.title, b.isbn, b.category, b.publication_year, b.copies_available
                FROM books b
            """)
            return [Book(*row) for row in cur.fetchall()]

    def search(self, keyword):
        if not self.conn:
            return []
        with self.conn.cursor() as cur:
            query = """
                SELECT b.book_id, b.title, b.isbn, b.category, b.publication_year, b.copies_available
                FROM books b
                JOIN book_authors ba ON b.book_id = ba.book_id
                JOIN authors a ON ba.author_id = a.author_id
                WHERE LOWER(b.title) LIKE %s OR LOWER(a.name) LIKE %s
            """
            cur.execute(query, (f"%{keyword.lower()}%", f"%{keyword.lower()}%"))
            return [Book(*row) for row in cur.fetchall()]

    def add_book(self, title, isbn, category, publication_year, copies_available, author_ids):
        if not self.conn:
            return False
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO books (title, isbn, category, publication_year, copies_available)
                    VALUES (%s, %s, %s, %s, %s) RETURNING book_id
                """, (title, isbn, category, publication_year, copies_available))
                book_id = cur.fetchone()[0]
                for author_id in author_ids:
                    cur.execute("INSERT INTO book_authors (book_id, author_id) VALUES (%s, %s)", (book_id, author_id))
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False

