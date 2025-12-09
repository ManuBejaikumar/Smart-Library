from db_connection import get_connection
from models.User import User
from models.Librarian import Librarian
from models.Member import Member

class UserDAO:
    def __init__(self):
        self.conn = get_connection()

    def authenticate(self, username, password):
        if not self.conn:
            return None
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    SELECT u.user_id, u.password_hash, u.role, m.member_id, m.full_name, m.email, m.phone
                    FROM users u
                    LEFT JOIN members m ON u.user_id = m.user_id
                    WHERE u.username = %s
                """, (username,))
                row = cur.fetchone()
                if row and User.check_password(row[1], password):
                    user_id, _, role = row[0], row[2], row[2]
                    if role == 'librarian':
                        user = Librarian(user_id, username)
                    else:  # member
                        member_id, full_name, email, phone = row[3], row[4], row[5], row[6]
                        user = Member(user_id, username, full_name, email, phone)
                        user.member_id = member_id
                    user.role = role
                    return user
        except Exception as e:
            print("Auth error:", e)
        return None