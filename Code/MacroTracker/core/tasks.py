from rich import print  # Colored output.

class TaskManager:

    @staticmethod
    def add_task(user_data, db, username):
        name = input("Task Name: ").strip()
        deadline = input("Deadline (YYYY-MM-DD): ").strip()

        if not name or not deadline:
            print("[red]Invalid input[/red]")
            return

        data = db.load()

        data[username]["tasks"].append({
            "name": name,
            "deadline": deadline,
            "completed": False
        })

        db.save(data)
        print("[green]Task added![/green]")

    @staticmethod
    def view_tasks(user_data):
        tasks = user_data.get("tasks", [])

        if not tasks:
            print("[red]No tasks[/red]")
            return

        for i, t in enumerate(tasks):
            status = "✔" if t["completed"] else "✖"
            print(f"{i+1}. {t['name']} - {t['deadline']} [{status}]")

    @staticmethod
    def complete_task(user_data, db, username):
        tasks = user_data.get("tasks", [])

        if not tasks:
            print("[red]No tasks[/red]")
            return

        for i, t in enumerate(tasks):
            print(f"{i+1}. {t['name']}")

        try:
            choice = int(input("Select task: ")) - 1
        except:
            print("[red]Invalid input[/red]")
            return

        data = db.load()

        if 0 <= choice < len(tasks):
            data[username]["tasks"][choice]["completed"] = True
            db.save(data)
            print("[green]Task completed![/green]")
        else:
            print("[red]Invalid choice[/red]")
