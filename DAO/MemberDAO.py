from db_connection import get_connection
from models.Member import Member

class MemberDAO:
    def __init__(self):
        self.conn = get_connection()

    def get_all(self):
        if not self.conn:
            return []
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT m.member_id, u.user_id, u.username, m.full_name, m.email, m.phone
                FROM members m JOIN users u ON m.user_id = u.user_id
            """)
            rows = cur.fetchall()
            return [Member(row[1], row[2], row[3], row[4], row[5]) for row in rows]

    def add_member(self, username, password, full_name, email, phone):
        if not self.conn:
            return False
        try:
            with self.conn.cursor() as cur:
                hashed_pw = Member.hash_password(password)
                cur.execute("""
                    INSERT INTO users (username, password_hash, role) 
                    VALUES (%s, %s, 'member') RETURNING user_id
                """, (username, hashed_pw))
                user_id = cur.fetchone()[0]
                cur.execute("""
                    INSERT INTO members (user_id, full_name, email, phone)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, full_name, email, phone))
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False