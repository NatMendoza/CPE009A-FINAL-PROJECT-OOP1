import time
from data.database import Database
from authentication.user import User
from authentication.admin import Admin
from rich import print

SECRET_CODE = "MacroTrackerAdmin"

class AuthSystem:

    def __init__(self):
        self.db = Database()

    def log(self, message):
        with open("logs.txt", "a") as f:
            f.write(f"{time.ctime()} - {message}\n")

    def register_user(self):
        username = input("Username: ")
        password = input("Password: ")

        user = User(username, password)

        if self.db.create_user(username, password, user.get_role()):
            print("[green]User registered![/green]")
            self.log(f"User registered: {username}")
        else:
            print("[red]User already exists[/red]")

        time.sleep(1)

    def register_admin(self):
        code = input("Enter Admin Secret Code: ")

        if code != SECRET_CODE:
            print("[red]Invalid admin code[/red]")
            return

        username = input("Admin Username: ")
        password = input("Password: ")

        admin = Admin(username, password)
        admin_id = admin.get_admin_id()

        if self.db.create_user(username, password, admin.get_role(), admin_id):
            print(f"[green]Admin registered! Your ID: {admin_id}[/green]")
            self.log(f"Admin registered: {username}")
        else:
            print("[red]Admin already exists[/red]")

    def login(self):
        username = input("Username: ")
        password = input("Password: ")

        user = self.db.get_user(username)

        if not user or user["password"] != password:
            print("[red]Invalid credentials[/red]")
            return None, None

        if user["role"] == "admin":
            admin_id = input("Enter Admin ID: ")
            if str(user["admin_id"]) != admin_id:
                print("[red]Invalid Admin ID[/red]")
                return None, None

        print("[green]Login successful![/green]")
        return username, user["role"]
