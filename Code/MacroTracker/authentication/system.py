from data.database import Database

db = Database()

class AuthSystem:

    def register(self):
        u = input("User: ")
        p = input("Pass: ")

        data = db.load()
        data[u] = p
        db.save(data)

    def login(self):
        u = input("User: ")
        p = input("Pass: ")

        data = db.load()

        if u in data and data[u] == p:
            print("Login success")
            return True
