from models.person import Person                # This imports the base class.

class User(Person):                             # INHERITANCE applied, the user inherits from person.

    def __init__(self, username, password):
        super().__init__(username, password)    # Initializes username and password.

    def get_role(self):                         # POLYMORPHISM used, which defines the role.
        return "user"
