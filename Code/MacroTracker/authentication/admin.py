import random
from models.person import Person

class Admin(Person):   # INHERITANCE

    def __init__(self, username, password):
        super().__init__(username, password)
        self.__admin_id = random.randint(1000, 999999)  # ENCAPSULATION

    def get_role(self):   # POLYMORPHISM
        return "admin"

    def get_admin_id(self):
        return self.__admin_id
