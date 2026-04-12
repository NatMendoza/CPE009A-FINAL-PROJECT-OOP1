from models.person import Person

class User(Person):   # INHERITANCE

    def __init__(self, username, password):
        super().__init__(username, password)

    def get_role(self):   # POLYMORPHISM
        return "user"
