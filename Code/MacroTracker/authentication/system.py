from data.database import Database
from rich import print

db = Database()

class AuthSystem:

    def register(self):
        username = input("Username: ")
        password = input("Password: ")

        if db.create_user(username, password):
            print("[green]User registered![/green]")
        else:
            print("[red]User already exists[/red]")

    def login(self):
        username = input("Username: ")
        password = input("Password: ")

        stored = db.get_user(username)

        if stored and stored == password:
            print("[green]Login successful![/green]")
            return username
        else:
            print("[red]Invalid credentials[/red]")
            return None

    def update(self):
        username = input("Username: ")
        new_pass = input("New Password: ")

        if db.update_user(username, new_pass):
            print("[yellow]Updated successfully[/yellow]")
        else:
            print("[red]User not found[/red]")

    def delete(self):
        username = input("Username: ")

        if db.delete_user(username):
            print("[red]User deleted[/red]")
        else:
            print("[red]User not found[/red]")
