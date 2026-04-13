from rich import print

class HealthAdvisor:

    @staticmethod
    def show(cal, sugar, fat):
        print("\n[bold yellow]Health Advice[/bold yellow]")

        if cal > 3000:
            print("[red]Reduce calorie intake[/red]")
        else:
            print("[green]Calories are okay[/green]")

        if sugar > 50:
            print("[red]Cut down sugary foods[/red]")

        if fat > 70:
            print("[red]Lower fat consumption[/red]")

    @staticmethod
    def bmi_advice(bmi):
        print("\n[bold yellow]BMI Advice[/bold yellow]")

        if bmi < 18.5:
            print("Eat more nutritious food")
        elif bmi < 25:
            print("Maintain your lifestyle")
        else:
            print("Exercise more and reduce calories")
            
