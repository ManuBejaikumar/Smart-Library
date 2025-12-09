import bcrypt

class User:
    def __init__(self, user_id, username, role):
        self.user_id = user_id
        self.username = username
        self.role = role

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def check_password(stored_hash, password):
        # Temporary plain-text check for quick testing
        return stored_hash == password