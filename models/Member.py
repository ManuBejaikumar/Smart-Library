from models.User import User

class Member(User):
    def __init__(self, user_id, username, full_name, email, phone):
        super().__init__(user_id, username, 'member')
        self.full_name = full_name
        self.email = email
        self.phone = phone