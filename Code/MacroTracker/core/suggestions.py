from rich import print

class HealthAdvisor:
    @staticmethod
    def show(cal, sugar, fat):
        print("\n[bold yellow]Health Advice[/bold yellow]")

        if cal > 4000:
            print("[red]High calories[/red]")
        if sugar > 50:
            print("[red]Too much sugar[/red]")
        if fat > 70:
            print("[red]Too much fat[/red]")

        if cal <= 4000 and sugar <= 50 and fat <= 70:
            print("[green]Balanced diet[/green]")
