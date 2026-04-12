from rich.console import Console
import questionary
import pyfiglet

from authentication.system import AuthSystem
from core.tracker import Tracker
from core.bmi import BMI
from core.suggestions import HealthAdvisor
from models.macros import FoodItem

console = Console()

def show_title():
    console.print(pyfiglet.figlet_format("MacroTracker"), style="cyan")

def main():
    auth = AuthSystem()
    tracker = Tracker()

    show_title()

    while True:
        choice = questionary.select(
            "Select Option:",
            choices=[
                "Register",
                "Login",
                "Add Food",
                "View History",
                "Calculate Total",
                "BMI Check",
                "Exit"
            ]
        ).ask()

        if choice == "Register":
            auth.register()

        elif choice == "Login":
            auth.login()

        elif choice == "Add Food":
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

        elif choice == "View History":
            tracker.show_history()

        elif choice == "Calculate Total":
            cal = sum(f.calories for f in tracker.history)
            sugar = sum(f.sugar for f in tracker.history)
            fat = sum(f.fat for f in tracker.history)

            console.print(f"[bold]Total Calories:[/bold] {cal:.2f}")
            HealthAdvisor.show(cal, sugar, fat)

        elif choice == "BMI Check":
            w = float(input("Weight: "))
            h = float(input("Height: "))
            bmi = BMI.compute(w, h)

            console.print(f"BMI: {bmi:.2f}")
            console.print(BMI.advice(bmi))

        elif choice == "Exit":
            console.print("[red]Goodbye![/red]")
            break

if __name__ == "__main__":
    main()
