import os
import time
import questionary
import pyfiglet
from rich.console import Console

from authentication.system import AuthSystem
from core.tracker import Tracker
from core.bmi import BMI
from core.suggestions import HealthAdvisor
from models.macros import FoodItem

console = Console()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_title():
    console.print(pyfiglet.figlet_format("MacroTracker"), style="cyan")

def pause():
    input("\nPress Enter to continue...")

def main():
    auth = AuthSystem()
    tracker = Tracker()

    current_user = None
    role = None

    while True:
        clear()
        show_title()

        # 🔐 NOT LOGGED IN MENU
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
                auth.register_admin()   # THIS SHOWS ADMIN ID AFTER
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

            # ADMIN MENU
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
                    clear()
                    show_title()
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
                    auth.delete(username)
                    pause()

                elif choice == "Logout":
                    current_user = None
                    role = None

            # USER MENU
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

                    food = FoodItem(
                        name, cal, carbs, sugar, fiber, protein, fat, water, grams
                    )

                    tracker.add_food(food.compute_scaled())
                    console.print("[green]Food added![/green]")
                    time.sleep(1)
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
                    auth.delete(current_user)
                    current_user = None
                    role = None
                    pause()

                elif choice == "Logout":
                    current_user = None
                    role = None

if __name__ == "__main__":
    main()
