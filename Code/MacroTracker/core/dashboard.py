from rich import print                                                   # Styled terminal output.
import random                                                            # Random motivational messages.
import calendar                                                          # Calendar display system.
import datetime                                                          # Date tracking.

class Dashboard:

    @staticmethod
    def show(user_data):
        print("\n[bold cyan]=== DASHBOARD ===[/bold cyan]")

        history = user_data.get("history", [])

        total_cal = sum(item["calories"] for item in history)
        # Computes total calories from food history.

        print(f"[green]Calories:[/green] {total_cal}")
        print(f"[yellow]Streak:[/yellow] {user_data.get('streak', 0)}")

        messages = [
            "Keep going!",
            "You're improving!",
            "Stay consistent!"
        ]

        print(f"[magenta]{random.choice(messages)}[/magenta]")
        # Random motivational message.

    @staticmethod
    def calendar(user_data):
        print("\n[bold cyan]=== CALENDAR ===[/bold cyan]")

        days = user_data.get("active_days", [])

        month = calendar.monthcalendar(datetime.date.today().year,
                                       datetime.date.today().month)
        # Generates full month calendar.

        print("Su Mo Tu We Th Fr Sa")

        for week in month:
            for day in week:
                if day == 0:
                    print("  ", end=" ")
                elif str(day) in days:
                    print(f"[green]{day:2}[/green]", end=" ")
                else:
                    print(f"[red]{day:2}[/red]", end=" ")
            print()
