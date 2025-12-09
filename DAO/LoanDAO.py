from db_connection import get_connection
from models.Loan import Loan
from datetime import date


class LoanDAO:
    def __init__(self):
        self.conn = get_connection()


    def get_loans_for_member(self, member_id):
        return self.get_active_loans(member_id)

    def borrow_book(self, book_id, member_id):
        if not self.conn:
            return False
        try:
            with self.conn.cursor() as cur:

                cur.execute("SELECT copies_available FROM books WHERE book_id = %s", (book_id,))
                copies = cur.fetchone()[0]
                if copies <= 0:
                    return False


                cur.execute("SELECT COUNT(*) FROM loans WHERE member_id = %s AND return_date IS NULL", (member_id,))
                active_loans = cur.fetchone()[0]
                if active_loans >= 3:
                    return False


                loan_date = date.today()
                due_date = Loan.calculate_due_date(loan_date)
                cur.execute("""
                            INSERT INTO loans (book_id, member_id, loan_date, due_date)
                            VALUES (%s, %s, %s, %s)
                            """, (book_id, member_id, loan_date, due_date))


                cur.execute("UPDATE books SET copies_available = copies_available - 1 WHERE book_id = %s", (book_id,))
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False

    def return_book(self, loan_id):
        if not self.conn:
            return False
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT book_id FROM loans WHERE loan_id = %s AND return_date IS NULL", (loan_id,))
                row = cur.fetchone()
                if not row:
                    return False
                book_id = row[0]

                cur.execute("UPDATE loans SET return_date = CURRENT_DATE WHERE loan_id = %s", (loan_id,))
                cur.execute("UPDATE books SET copies_available = copies_available + 1 WHERE book_id = %s", (book_id,))
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False

    def get_active_loans(self, member_id=None):

        if not self.conn:
            return []
        with self.conn.cursor() as cur:
            if member_id is None:
                cur.execute("""
                    SELECT loan_id, book_id, member_id, loan_date, due_date, return_date
                    FROM loans WHERE return_date IS NULL
                """)
            else:
                cur.execute("""
                    SELECT loan_id, book_id, member_id, loan_date, due_date, return_date
                    FROM loans WHERE member_id = %s AND return_date IS NULL
                """, (member_id,))
            return [Loan(*row) for row in cur.fetchall()]