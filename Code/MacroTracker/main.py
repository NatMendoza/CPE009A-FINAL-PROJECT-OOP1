import os                                        # Terminal Clearing.
import time                                      # Timestamp for logs and delays (Waits for user input to proceed).
import random                                    # For random generation of ID for admin and color for display.
import questionary                               # Menu UI
import pyfiglet                                  # ASCII Titlte generation for MACROTRACKER display.
from rich.console import Console                 # Styled printing specifically colors output formatting.

from authentication.system import AuthSystem
from core.tracker import Tracker
from core.bmi import BMI
from core.suggestions import HealthAdvisor
from models.macros import FoodItem

console = Console()

# ================= CLEAR SCREEN =================
def clear():                                     # This basically clears terminal screen depending on the OS.
    os.system('cls' if os.name == 'nt' else 'clear')

# ================= TITLE (CHANGING COLOR) =================
def show_title():                                # This function basically random selects a color and prints macrotracker title display.
    colors = ["cyan", "green", "yellow", "magenta", "blue"]
    color = random.choice(colors)
    console.print(pyfiglet.figlet_format("MacroTracker"), style=color)

# ================= PAUSE =================
def pause():                                      # Pauses the program until pressed enter to proceed. (Basically waits user input)        
    input("\nPress Enter to continue...")

# ================= MAIN =================        # This is the main program function in combination of all the .py files which were organized into folders.
def main():
    auth = AuthSystem()                           # Handles the login/resigtration of the UI.
    tracker = Tracker()                           # Handles food history.

    current_user = None                           # Trackers the logged user
    role = None                                   # Trackers the user role whether if its user/admin.

    while True:                                   # Applies a loop which runs continuosly until met a condition.
        clear()
        show_title()

        # USER NOT LOGGED IN
        if not current_user:                      # The program will do if it is not logged in.

            choice = questionary.select(          # Choice display.    
                "Select Option:",
                choices=[
                    "Register User",
                    "Register Admin",
                    "Login",
                    "Exit"
                ]
            ).ask()

            if choice == "Register User":
                auth.register_user()                # Creating user account.
                pause()

            elif choice == "Register Admin":
                auth.register_admin()                # Creating administrator account.
                pause()

            elif choice == "Login":                  
                current_user, role = auth.login()    # User login.
                pause()

            elif choice == "Exit":        
                console.print("[red]Goodbye![/red]")  # Leaves the program / Quit.
                break

        # USER LOOGGED IN
        else:
            clear()
            show_title()

            # ================= ADMIN =================
            if role == "admin":                        # If it is admin then it will show Admin menu.

                choice = questionary.select(
                    f"[ADMIN] {current_user}",
                    choices=[
                        "View Logs",
                        "View History",
                        "Delete User",
                        "Logout"
                    ]
                ).ask()

                if choice == "View Logs":                # This opens the data inside the text file which can be also edited through the main text file.
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
            else:                                          # If user is not an admin then displays user menu.

                choice = questionary.select(               # This provides the user menu choices.
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

                if choice == "Add Food":                    # Creates food as "object"
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
                    tracker.add_food(food.compute_scaled())  # Adds the food to the history

                    console.print("[green]Food added![/green]")
                    pause()

                elif choice == "View History":               # Displays the food history
                    tracker.show_history()
                    pause()

                elif choice == "Delete Food Entry":          # Removes a food from a history (Application of CRUD + Additionally, it might have contained a wrong input)
                    tracker.delete_food()
                    pause()

                elif choice == "Calculate Total":            # Gets the sum
                    cal = sum(f.calories for f in tracker.history)
                    sugar = sum(f.sugar for f in tracker.history)
                    fat = sum(f.fat for f in tracker.history)

                    console.print(f"Total Calories: {cal:.2f}")
                    HealthAdvisor.show(cal, sugar, fat)
                    pause()

                elif choice == "BMI Check":                    # Calculates the Body Mass Index (In reference to the actual BMI Sheet)
                    w = float(input("Weight in kg: "))
                    h = float(input("Height in meters: "))
                    bmi = BMI.compute(w, h)

                    console.print(f"BMI: {bmi:.2f}")
                    HealthAdvisor.bmi_advice(bmi)               # Program provides and shows "possible" suggestiongs to user.
                    pause()

                elif choice == "Delete Account":                # Account deletion (Application of CRUD?) 
                    confirm = input("Are you sure you want to delete this account? (y/n): ")

                    if confirm.lower() == "y":
                        auth.db.delete_user(current_user)
                        auth.log(f"Deleted account: {current_user}")
                        console.print("[red]Account deleted[/red]")
                        current_user = None
                        role = None
                    pause()

                elif choice == "Logout":                          # Resets the user and role which go back to the loop.
                    current_user = None
                    role = None


if __name__ == "__main__":
    main()                                                         # RUNS THE PROGRAM.
