import os                                        # Used to clear terminal screen depending on OS.
import time                                      # Used for delay (pause effect).
import random                                    # Used to randomize title color.
import questionary                               # Provides interactive CLI menu.
import pyfiglet                                  # Creates ASCII art title.
from rich.console import Console                 # Allows colored/styled output.

from authentication.system import AuthSystem     # Handles login/register system.
from core.tracker import Tracker                 # Handles food tracking.
from core.bmi import BMI                         # BMI computation logic.
from core.suggestions import HealthAdvisor       # Health suggestions.
from core.dashboard import Dashboard             # Dashboard system (NEW).
from core.tasks import TaskManager               # Task system (NEW).
from models.macros import FoodItem               # Food object model.
from core.activity_tracker import PhysicalActivityTracker
console = Console()                              # Initialize rich console.

# ================= CLEAR SCREEN =================
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clears terminal screen.

# ================= TITLE =================
def show_title():
    colors = ["cyan", "green", "yellow", "magenta", "blue"]  # List of colors.
    console.print(pyfiglet.figlet_format("MacroTracker"), style=random.choice(colors))  # Random color title.

# ================= PAUSE =================
def pause():
    input("\nPress Enter to continue...")        # Waits for user input.

# ================= MAIN =================
def main():
    auth = AuthSystem()                         # Handles authentication logic.
    tracker = Tracker()                         # Handles food tracking.

    current_user = None                         # Stores current logged-in user.
    role = None                                 # Stores role (user/admin).

    while True:                                 # Infinite loop for program.
        clear()
        show_title()

        # ================= NOT LOGGED IN =================
        if not current_user:

            choice = questionary.select(
                "Select Option:",
                choices=["Register User", "Register Admin", "Login", "Exit"]
            ).ask()

            if choice == "Register User":
                auth.register_user()            # Calls user registration.
                pause()

            elif choice == "Register Admin":
                auth.register_admin()           # Calls admin registration.
                pause()

            elif choice == "Login":
                current_user, role = auth.login()  # Login returns username + role.
                pause()

            elif choice == "Exit":
                console.print("[red]Goodbye![/red]")
                break

        # ================= LOGGED IN =================
        else:
            clear()
            show_title()

            user_data = auth.db.get_user(current_user)  # Fetch user data.

            # ================= ADMIN =================
            if role == "admin":

                choice = questionary.select(
                    f"[ADMIN] {current_user}",
                    choices=["View Logs", "View All Users", "Delete User", "Logout"]
                ).ask()

                if choice == "View Logs":
                    try:
                        with open("logs.txt", "r") as f:   # Open logs file.
                            print(f.read())
                    except:
                        print("No logs yet.")
                    pause()

                elif choice == "View All Users":
                    data = auth.db.load()                 # Load all users.
                    for user in data:
                        print(user, "-", data[user]["role"])  # Show username + role.
                    pause()

                elif choice == "Delete User":              # Deletes User
                    username = input("Enter username: ")   # Input Registered User to delete
                    confirm = input("Are you sure? (y/n): ")  # Confirmation of deleting User

                    if confirm.lower() == "y":
                        if auth.db.delete_user(username):
                            auth.log(f"Deleted user: {username}")  # Log action.
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
                        "Dashboard", "Calendar",
                        "Add Food", "View History", "Delete Food Entry",
                        "Calculate Total", "BMI Check",
                        "Add Task", "View Tasks", "Complete Task",
                        "Delete Account", "Logout"
                    ]
                ).ask()

                # DASHBOARD
                if choice == "Dashboard":
                    Dashboard.show(user_data)   # Show stats + motivation.
                    pause()

                elif choice == "Calendar":
                    Dashboard.calendar(user_data)  # Show calendar.
                    pause()

                # FOOD SYSTEM
                elif choice == "Add Food":
                    try:
                        name = input("Food: ")
                        cal = float(input("Calories: "))
                        carbs = float(input("Carbs: "))
                        sugar = float(input("Sugar: "))
                        fiber = float(input("Fiber: "))
                        protein = float(input("Protein: "))
                        fat = float(input("Fat: "))
                        water = float(input("Water: "))
                        grams = float(input("Grams: "))
                    except:
                        console.print("[red]Invalid input[/red]")
                        pause()
                        continue

                    food = FoodItem(name, cal, carbs, sugar, fiber, protein, fat, water, grams)
                    tracker.add_food(food.compute_scaled())

                    # Save to database
                    data = auth.db.load()
                    data[current_user]["history"].append({"name": name, "calories": cal})
                    auth.db.save(data)

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
                    try:
                        w = float(input("Weight: "))
                        h = float(input("Height: "))
                    except:
                        console.print("[red]Invalid input[/red]")
                        pause()
                        continue

                    bmi = BMI.compute(w, h)
                    console.print(f"BMI: {bmi:.2f}")
                    HealthAdvisor.bmi_advice(bmi)
                    pause()
                    
                    #ACTIVITY TRACKER
                elif choice == "Physical Activity Tracker":
                    activity_tracker.dashboard(clear, show_title, console, pause)  

                # TASK SYSTEM
                elif choice == "Add Task":
                    TaskManager.add_task(user_data, auth.db, current_user)
                    pause()

                elif choice == "View Tasks":
                    TaskManager.view_tasks(user_data)
                    pause()

                elif choice == "Complete Task":
                    TaskManager.complete_task(user_data, auth.db, current_user)
                    pause()

                # DELETE ACCOUNT
                elif choice == "Delete Account":
                    confirm = input("Are you sure? (y/n): ")
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
    main()  # Runs the program
