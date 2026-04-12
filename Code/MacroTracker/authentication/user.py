from models.person import Person

class User(Person):
    def __init__(self, username, password):
        super().__init__(username, password)
