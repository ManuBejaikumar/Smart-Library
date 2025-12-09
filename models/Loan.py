from datetime import date, timedelta

class Loan:
    def __init__(self, loan_id, book_id, member_id, loan_date, due_date, return_date=None):
        self.loan_id = loan_id
        self.book_id = book_id
        self.member_id = member_id
        self.loan_date = loan_date
        self.due_date = due_date
        self.return_date = return_date

    @staticmethod
    def calculate_due_date(loan_date):
        return loan_date + timedelta(days=7)