import json
import os

FILE = "users.json"

class Database:

    @staticmethod
    def load():
        if not os.path.exists(FILE):
            return {}
        with open(FILE, "r") as f:
            return json.load(f)

    @staticmethod
    def save(data):
        with open(FILE, "w") as f:
            json.dump(data, f, indent=4)

    def create_user(self, username, password):
        data = self.load()
        if username in data:
            return False
        data[username] = password
        self.save(data)
        return True

    def get_user(self, username):
        data = self.load()
        return data.get(username)

    def update_user(self, username, password):
        data = self.load()
        if username in data:
            data[username] = password
            self.save(data)
            return True
        return False

    def delete_user(self, username):
        data = self.load()
        if username in data:
            del data[username]
            self.save(data)
            return True
        return False
