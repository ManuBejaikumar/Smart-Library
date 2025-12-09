from db_connection import get_connection
from models.BookClub import BookClub

class BookClubDAO:
    def __init__(self):
        self.conn = get_connection()

    def get_all(self):
        if not self.conn:
            return []
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT club_id, name, description, created_by, created_date
                FROM book_clubs
            """)
            return [BookClub(*row) for row in cur.fetchall()]

    def create_club(self, name, description, created_by):
        if not self.conn:
            return False
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO book_clubs (name, description, created_by)
                VALUES (%s, %s, %s) RETURNING club_id
            """, (name, description, created_by))
            club_id = cur.fetchone()[0]
            # Auto-join creator
            cur.execute("INSERT INTO club_members (club_id, member_id) VALUES (%s, %s)", (club_id, created_by))
        self.conn.commit()
        return True

    def join_club(self, club_id, member_id):
        if not self.conn:
            return False
        with self.conn.cursor() as cur:
            cur.execute("INSERT INTO club_members (club_id, member_id) VALUES (%s, %s) ON CONFLICT DO NOTHING", (club_id, member_id))
        self.conn.commit()
        return True