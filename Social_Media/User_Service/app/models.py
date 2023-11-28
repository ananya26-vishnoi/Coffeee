# app/models.py

from app import mongo

class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def save(self):
        mongo.db.users.insert_one({
            'username': self.username,
            'email': self.email,
            'password': self.password
        })

    @staticmethod
    def find_by_username(username):
        return mongo.db.users.find_one({'username': username})

    @staticmethod
    def find_by_email(email):
        return mongo.db.users.find_one({'email': email})
