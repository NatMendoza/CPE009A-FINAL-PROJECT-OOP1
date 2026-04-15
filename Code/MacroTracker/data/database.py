import json  # Used to store data in JSON file.
import os  # Checks if file exists.
import time  # Timestamp for created users.

FILE = "users.json"  # Database file.

class Database:

    @staticmethod
    def load():
        # Loads JSON database file.
        if not os.path.exists(FILE):
            return {}  # Returns empty if no file exists.

        with open(FILE, "r") as f:
            return json.load(f)

    @staticmethod
    def save(data):
        # Saves data back into JSON file.
        with open(FILE, "w") as f:
            json.dump(data, f, indent=4)

    def create_user(self, username, password, role="user", admin_id=None):
        data = self.load()

        if username in data:
            return False  # User already exists.

        data[username] = {
            "password": password,
            "role": role,
            "created_at": time.ctime(),

            # SYSTEM DATA
            "streak": 0,
            "last_login": None,
            "active_days": [],

            # FOOD + TASK STORAGE
            "history": [],
            "tasks": []
        }

        if role == "admin":
            data[username]["admin_id"] = admin_id

        self.save(data)
        return True

    def get_user(self, username):
        return self.load().get(username)
        # Returns specific user data.

    def delete_user(self, username):
        data = self.load()

        if username in data:
            del data[username]  # Deletes user.
            self.save(data)
            return True

        return False
