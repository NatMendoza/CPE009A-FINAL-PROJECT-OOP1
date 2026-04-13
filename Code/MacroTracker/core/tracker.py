from rich.table import Table
from rich.console import Console

console = Console()

class Tracker:
    def __init__(self):
        self.history = []

    def add_food(self, food):
        self.history.append(food)

    def show_history(self):
        if not self.history:
            console.print("[red]No records[/red]")
            return

        table = Table(title="Food History")

        table.add_column("Food")
        table.add_column("Calories")
        table.add_column("Protein")
        table.add_column("Fat")

        for f in self.history:
            table.add_row(
                f.name,
                f"{f.calories:.2f}",
                f"{f.protein:.2f}",
                f"{f.fat:.2f}"
            )

        console.print(table)

    def delete_food(self):
        if not self.history:
            console.print("[red]No records[/red]")
            return

        for i, f in enumerate(self.history):
            print(f"{i+1}. {f.name}")

        choice = int(input("Select item to delete: ")) - 1

        if 0 <= choice < len(self.history):
            del self.history[choice]
            console.print("[yellow]Deleted successfully[/yellow]")
        else:
            console.print("[red]Invalid choice[/red]")
