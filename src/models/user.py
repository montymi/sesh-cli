from pymongo import MongoClient

class User:
    def __init__(self):
        self.client = MongoClient('mongodb+srv://chandlercree:NU22ms0cc3rGK@seshdev.sc1qn4y.mongodb.net/?retryWrites=true&w=majority&appName=SeshDev')
        self.db = self.client['sesh_testing']
        self.collection = self.db['users'] 
        self.user = None

    def user_exists(self, username):
        return self.collection.find_one({"username": username}) is not None

    def create_user(self, username):
        try:
            if self.user_exists(username):
                return 0  # User already exists
            elif len(username) == 6:
                self.collection.insert_one({"username": username})
                return 1
            else:
                return -1
        except Exception as e:
            return -1  # An error occurred

    def authenticate_user(self, username):
        return bool(self.collection.find_one({"username": username}))