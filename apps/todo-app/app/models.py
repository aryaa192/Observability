from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from app import mongo

class User:
    @staticmethod
    def create_user(username, password):
        password_hash = generate_password_hash(password)
        mongo.db.users.insert_one({'username': username, 'password': password_hash})

    @staticmethod
    def find_user(username):
        return mongo.db.users.find_one({'username': username})

    @staticmethod
    def check_password(username, password):
        user = User.find_user(username)
        if user and check_password_hash(user['password'], password):
            return True
        return False

class Todo:
    @staticmethod
    def create_task(user_id, title, description):
        mongo.db.todos.insert_one({'user_id': user_id, 'title': title, 'description': description})

    @staticmethod
    def get_tasks(user_id):
        return mongo.db.todos.find({'user_id': user_id})
