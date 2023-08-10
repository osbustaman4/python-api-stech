from flask_login import UserMixin

class Auth(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
        }