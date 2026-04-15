import questionary

class PhysicalActivityTracker:
    def __init__(self):
        self.recommendations = {
            "low": 30,
            "moderate": 20,
            "high": 10
        }
    def get_suggestion(self, intensity, time_minutes):
        recommended_time= self.recommendations[intensity]

        if time_minutes < recommended_time:
            return "Add more intensity or time."
        elif time_minutes > recommended_time * 1.5:
            return "Slow down, you are over exercising."
        else:
            return "Great job!"

    def dashboard(self, clear, show_title, console, pause):
        while True:
            clear()
            show_title()

            choice = questionary.select(
                "Physical Activity Tracker:",
                choices=["Log Activity", "Back"]
            ).ask()

            if choice == "Log Activity":
                activity_type = questionary.select(
                    "Activity type:",
                    choices=["cardio", "weightlifting"]
                ).ask()

                intensity= questionary.select(
                    "Intensity:",
                    choices=["low", "moderate", "high"]
                ).ask()

                try:
                    time_minutes= float(input("Time (minutes): "))
                    if time_minutes<= 0:
                        raise ValueError
                except:
                    console.print("[red]Invalid input[/red]")
                    pause()
                    continue
                suggestion = self.get_suggestion(intensity, time_minutes)

                console.print(f"Type: {activity_type}")
                console.print(f"Intensity: {intensity}")
                console.print(f"Time: {time_minutes}")
                console.print(f"Suggestion: {suggestion}")

                pause()
            elif choice == "Back":
                break
