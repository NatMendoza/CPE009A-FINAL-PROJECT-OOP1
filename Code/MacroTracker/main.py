import os
import time
import random
import questionary
import pyfiglet
from rich.console import Console

from authentication.system import AuthSystem
from core.tracker import Tracker
from core.bmi import BMI
from core.suggestions import HealthAdvisor
from models.macros import FoodItem

console = Console()

# ================= CLEAR SCREEN =================
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# ================= TITLE (CHANGING COLOR) =================
def show_title():
    colors = ["cyan", "green", "yellow", "magenta", "blue"]
    color = random.choice(colors)
    console.print(pyfiglet.figlet_format("MacroTracker"), style=color)

# ================= PAUSE =================
def pause():
    input("\nPress Enter to continue...")

# ================= MAIN =================
def main():
    auth = AuthSystem()
    tracker = Tracker()

    current_user = None
    role = None

    while True:
        clear()
        show_title()

        # 🔐 NOT LOGGED IN
        if not current_user:

            choice = questionary.select(
                "Select Option:",
                choices=[
                    "Register User",
                    "Register Admin",
                    "Login",
                    "Exit"
                ]
            ).ask()

            if choice == "Register User":
                auth.register_user()
                pause()

            elif choice == "Register Admin":
                auth.register_admin()
                pause()

            elif choice == "Login":
                current_user, role = auth.login()
                pause()

            elif choice == "Exit":
                console.print("[red]Goodbye![/red]")
                break

        # 🔓 LOGGED IN
        else:
            clear()
            show_title()

            # ================= ADMIN =================
            if role == "admin":

                choice = questionary.select(
                    f"[ADMIN] {current_user}",
                    choices=[
                        "View Logs",
                        "View History",
                        "Delete User",
                        "Logout"
                    ]
                ).ask()

                if choice == "View Logs":
                    try:
                        with open("logs.txt", "r") as f:
                            print(f.read())
                    except:
                        print("No logs yet.")
                    pause()

                elif choice == "View History":
                    tracker.show_history()
                    pause()

                elif choice == "Delete User":
                    username = input("Enter username to delete: ")
                    confirm = input("Are you sure? (y/n): ")

                    if confirm.lower() == "y":
                        if auth.db.delete_user(username):
                            auth.log(f"Deleted user: {username}")
                            console.print("[red]User deleted[/red]")
                        else:
                            console.print("[red]User not found[/red]")
                    pause()

                elif choice == "Logout":
                    current_user = None
                    role = None

            # ================= USER =================
            else:

                choice = questionary.select(
                    f"Welcome {current_user}",
                    choices=[
                        "Add Food",
                        "View History",
                        "Delete Food Entry",
                        "Calculate Total",
                        "BMI Check",
                        "Delete Account",
                        "Logout"
                    ]
                ).ask()

                if choice == "Add Food":
                    name = input("Food: ")
                    cal = float(input("Calories: "))
                    carbs = float(input("Carbs: "))
                    sugar = float(input("Sugar: "))
                    fiber = float(input("Fiber: "))
                    protein = float(input("Protein: "))
                    fat = float(input("Fat: "))
                    water = float(input("Water: "))
                    grams = float(input("Grams: "))

                    food = FoodItem(name, cal, carbs, sugar, fiber, protein, fat, water, grams)
                    tracker.add_food(food.compute_scaled())

                    console.print("[green]Food added![/green]")
                    pause()

                elif choice == "View History":
                    tracker.show_history()
                    pause()

                elif choice == "Delete Food Entry":
                    tracker.delete_food()
                    pause()

                elif choice == "Calculate Total":
                    cal = sum(f.calories for f in tracker.history)
                    sugar = sum(f.sugar for f in tracker.history)
                    fat = sum(f.fat for f in tracker.history)

                    console.print(f"Total Calories: {cal:.2f}")
                    HealthAdvisor.show(cal, sugar, fat)
                    pause()

                elif choice == "BMI Check":
                    w = float(input("Weight: "))
                    h = float(input("Height: "))
                    bmi = BMI.compute(w, h)

                    console.print(f"BMI: {bmi:.2f}")
                    HealthAdvisor.bmi_advice(bmi)
                    pause()

                elif choice == "Delete Account":
                    confirm = input("Are you sure you want to delete this account? (y/n): ")

                    if confirm.lower() == "y":
                        auth.db.delete_user(current_user)
                        auth.log(f"Deleted account: {current_user}")
                        console.print("[red]Account deleted[/red]")
                        current_user = None
                        role = None
                    pause()

                elif choice == "Logout":
                    current_user = None
                    role = None


if __name__ == "__main__":
    main()
