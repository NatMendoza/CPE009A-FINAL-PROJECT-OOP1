class PhysicalActivityTracker:
    def __init__(self):
        self.recommendations = {
            "low": 30,
            "moderate": 20,
            "high": 10
        }

    def get_suggestion(self, intensity, time_minutes):
        recommended_time = self.recommendations[intensity]

        if time_minutes < recommended_time:
            return "Add more intensity or time."
        elif time_minutes > recommended_time * 1.5:
            return "Take it a bit slower."
        else:
            return "Great job. Keep it up!"

    def log_activity(self):
        clear()
        show_title()
        console.print("[bold cyan]Physical Activity Tracker[/bold cyan]")

        activity_type = questionary.select(
            "Select Activity Type:",
            choices=["Cardio", "Weightlifting"]
        ).ask()

        intensity = questionary.select(
            "Select Intensity Level:",
            choices=["Low", "Moderate", "High"]
        ).ask()

        try:
            time_minutes = float(input("Enter time in minutes: "))
            if time_minutes <= 0:
                raise ValueError
        except ValueError:
            console.print("[red]Invalid time input.[/red]")
            pause()
            return

        suggestion = self.get_suggestion(intensity.lower(), time_minutes)

        console.print("\n[bold green]Activity Summary[/bold green]")
        console.print(f"Type: {activity_type}")
        console.print(f"Intensity: {intensity}")
        console.print(f"Duration: {time_minutes} minutes")
        console.print(f"Suggestion: {suggestion}")

        pause()

    def dashboard(self):
        while True:
            clear()
            show_title()

            choice = questionary.select(
                "Physical Activity Dashboard:",
                choices=[
                    "Log Activity",
                    "Back"
                ]
            ).ask()

            if choice == "Log Activity":
                self.log_activity()
            elif choice == "Back":
                break
