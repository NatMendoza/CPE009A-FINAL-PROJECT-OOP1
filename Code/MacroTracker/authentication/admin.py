import random                                            # This module allows generation of random numbers.
from models.person import Person                         # Imports the base class.

class Admin(Person):                                     # This performs INHERITANCE in application to OOP, which Admin inherits from person.

    def __init__(self, username, password):
        super().__init__(username, password)
        self.__admin_id = random.randint(1000, 999999)   # ENCAPSULATION is applied, which generates a random admin identification ID under private sector.

    def get_role(self):                                  # POLYMORPHISM applied, basically a subclass from a parent class person.
        return "admin"

    def get_admin_id(self):                              # This provides access to the private admin ID.
        return self.__admin_id
