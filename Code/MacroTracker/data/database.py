import json

class Database:
    def save(self, data):
        with open("users.json", "w") as f:
            json.dump(data, f)

    def load(self):
        try:
            with open("users.json", "r") as f:
                return json.load(f)
        except:
            return {}
