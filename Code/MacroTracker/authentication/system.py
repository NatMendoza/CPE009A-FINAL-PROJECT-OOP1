import time  # Used for logs and timestamps.
import datetime  # Used for streak tracking.

from data.database import Database  # Database system.
from authentication.user import User  # User object.
from authentication.admin import Admin  # Admin object.
from rich import print  # Colored terminal output.

SECRET_CODE = "MacroTrackerAdmin"  # Secret key for admin registration.

class AuthSystem:

    def __init__(self):
        self.db = Database()  # Connects system to database file.

    def log(self, message):
        # Writes system logs to logs.txt file.
        with open("logs.txt", "a") as f:
            f.write(f"{time.ctime()} - {message}\n")

    def register_user(self):
        username = input("Username: ").strip()  # Get username input.
        password = input("Password: ").strip()  # Get password input.

        if not username or not password:
            print("[red]Empty input not allowed[/red]")
            return  # Stops function if invalid input.

        user = User(username, password)  # Creates user object.

        if self.db.create_user(username, password, user.get_role()):
            print("[green]User registered![/green]")
            self.log(f"User registered: {username}")
        else:
            print("[red]User already exists[/red]")

    def register_admin(self):
        code = input("Enter Admin Secret Code: ")

        if code != SECRET_CODE:
            print("[red]Invalid admin code[/red]")
            return  # Stops if wrong secret code.

        username = input("Admin Username: ").strip()
        password = input("Password: ").strip()

        admin = Admin(username, password)  # Creates admin object.
        admin_id = admin.get_admin_id()  # Generates admin ID.

        if self.db.create_user(username, password, admin.get_role(), admin_id):
            print(f"[green]Admin created! ID: {admin_id}[/green]")
            self.log(f"Admin registered: {username}")
        else:
            print("[red]Admin already exists[/red]")

    def login(self):
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        user = self.db.get_user(username)

        if not user or user["password"] != password:
            print("[red]Invalid credentials[/red]")
            return None, None

        # Admin verification
        if user["role"] == "admin":
            admin_id = input("Enter Admin ID: ")
            if str(user["admin_id"]) != admin_id:
                print("[red]Wrong Admin ID[/red]")
                return None, None

        # STREAK SYSTEM
        data = self.db.load()
        user_data = data[username]

        today = datetime.date.today().day
        last = user_data.get("last_login")

        if last:
            last_day = int(last.split("-")[2])
            if today == last_day + 1:
                user_data["streak"] += 1
            elif today != last_day:
                user_data["streak"] = 1
        else:
            user_data["streak"] = 1

        user_data["last_login"] = str(datetime.date.today())

        if str(today) not in user_data["active_days"]:
            user_data["active_days"].append(str(today))

        self.db.save(data)

        print("[green]Login successful![/green]")
        return username, user["role"]
