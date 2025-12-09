from models.User import User

class Librarian(User):
    def __init__(self, user_id, username):
        super().__init__(user_id, username, 'librarian')