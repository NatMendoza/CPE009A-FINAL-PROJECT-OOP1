class Tracker:
    def __init__(self):
        self.history = []

    def add_food(self, food, cal):
        self.history.append((food, cal))

    def show(self):
        print(self.history)
